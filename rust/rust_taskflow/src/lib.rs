use async_trait::async_trait;
use std::collections::BTreeSet;
use std::future::Future;
use std::pin::Pin;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::task::{spawn, yield_now, JoinError, JoinHandle};
use tokio::time::sleep;

#[derive(PartialEq, Eq)]
pub enum PollStatus {
    NotRunning,
    Running,
    Finished,
}

#[async_trait]
pub trait TaskTrait {
    type Output;
    fn launch_task(&mut self);
    async fn poll_task(&mut self) -> Result<PollStatus, JoinError>;
    fn get_data(&self) -> Option<&Self::Output>;
}

pub struct Task<T, F>
where
    T: Send + 'static,
    F: FnOnce() -> Pin<Box<dyn Future<Output = T> + Send>> + Send + 'static,
{
    data: Option<T>,
    task: Option<F>,
    handle: Option<JoinHandle<T>>,
    finished: Arc<AtomicBool>,
}

impl<T, F> Default for Task<T, F>
where
    T: Send + 'static,
    F: FnOnce() -> Pin<Box<dyn Future<Output = T> + Send>> + Send + 'static,
{
    fn default() -> Self {
        Self {
            data: None,
            task: None,
            handle: None,
            finished: Arc::new(AtomicBool::new(false)),
        }
    }
}

impl<T, F> Task<T, F>
where
    T: Send + 'static,
    F: FnOnce() -> Pin<Box<dyn Future<Output = T> + Send>> + Send + 'static,
{
    pub fn new(task: F) -> Self {
        Self {
            task: Some(task),
            ..Self::default()
        }
    }

    pub fn get_data(&self) -> Option<&T> {
        self.data.as_ref()
    }
}

#[async_trait]
impl<T, F> TaskTrait for Task<T, F>
where
    T: Send + 'static,
    F: FnOnce() -> Pin<Box<dyn Future<Output = T> + Send>> + Send + 'static,
{
    type Output = T;
    fn launch_task(&mut self) {
        let finished = self.finished.clone();
        if let Some(task) = self.task.take() {
            let future = task();
            self.handle.replace(spawn(async move {
                let result = future.await;
                finished.store(true, Ordering::SeqCst);
                result
            }));
        }
    }

    async fn poll_task(&mut self) -> Result<PollStatus, JoinError> {
        if self.task.is_some() {
            Ok(PollStatus::NotRunning)
        } else if self.data.is_some() {
            Ok(PollStatus::Finished)
        } else if self
            .finished
            .compare_exchange_weak(true, false, Ordering::SeqCst, Ordering::SeqCst)
            .unwrap()
        {
            if let Some(handle) = self.handle.take() {
                self.data.replace(handle.await?);
            }
            Ok(PollStatus::Finished)
        } else {
            Ok(PollStatus::Running)
        }
    }

    fn get_data(&self) -> Option<&Self::Output> {
        self.get_data()
    }
}

pub struct TaskNode<'a, T>
where
    T: Send + 'static,
{
    task: Option<&'a mut dyn TaskTrait<Output = T>>,
    index: Option<usize>,
    children: BTreeSet<usize>,
    parents: BTreeSet<usize>,
}

impl<'a, T> Default for TaskNode<'a, T>
where
    T: Send + 'static,
{
    fn default() -> Self {
        Self {
            task: None,
            index: None,
            children: BTreeSet::default(),
            parents: BTreeSet::default(),
        }
    }
}

impl<'a, T> TaskNode<'a, T>
where
    T: Send + 'static,
{
    pub fn from_task<F>(task: &'a mut Task<T, F>) -> Self
    where
        F: FnOnce() -> Pin<Box<dyn Future<Output = T> + Send>> + Send + 'static,
    {
        Self {
            task: Some(task),
            ..Self::default()
        }
    }

    #[must_use]
    pub fn get_data(&self) -> Option<&T> {
        self.task.as_ref().and_then(|task| task.get_data())
    }
}

pub struct TaskGraph<'a, T>
where
    T: Send + 'static,
{
    tasks: Vec<TaskNode<'a, T>>,
    pending: BTreeSet<usize>,
    orphans: Vec<usize>,
    running: BTreeSet<usize>,
    completed: Vec<usize>,
}

impl<T> Default for TaskGraph<'_, T>
where
    T: Send + 'static,
{
    fn default() -> Self {
        Self {
            tasks: Vec::new(),
            pending: BTreeSet::new(),
            orphans: Vec::new(),
            running: BTreeSet::new(),
            completed: Vec::new(),
        }
    }
}

impl<'a, T> TaskGraph<'a, T>
where
    T: Send + 'static,
{
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    #[must_use]
    pub fn get_node_by_index(&self, idx: usize) -> Option<&TaskNode<'a, T>> {
        self.tasks.get(idx)
    }

    pub fn create_child(&mut self, mut node: TaskNode<'a, T>) -> usize {
        let index = self.tasks.len();
        node.index.replace(index);
        self.tasks.push(node);
        self.pending.insert(index);
        index
    }

    /// # Panics
    /// It does
    pub fn attach_child_to_parent(&mut self, parent_index: usize, child_index: usize) -> bool {
        if parent_index < self.tasks.len() && child_index < self.tasks.len() {
            let parent = self.tasks.get_mut(parent_index).unwrap();
            parent.children.insert(child_index);
            let child = self.tasks.get_mut(child_index).unwrap();
            child.parents.insert(parent_index);
            true
        } else {
            false
        }
    }

    pub fn push_node(
        &mut self,
        parent_index: Option<usize>,
        child: TaskNode<'a, T>,
    ) -> Option<usize> {
        let child_index = self.create_child(child);
        if let Some(parent_index) = parent_index {
            if self.attach_child_to_parent(parent_index, child_index) {
                Some(child_index)
            } else {
                None
            }
        } else {
            Some(child_index)
        }
    }

    pub fn init(&mut self) {
        self.pending = self.tasks.iter().filter_map(|task| task.index).collect();

        self.orphans = self
            .tasks
            .iter()
            .filter_map(|task| {
                if task.parents.is_empty() {
                    task.index
                } else {
                    None
                }
            })
            .collect();
        self.running.clear();
        self.completed.clear();
    }

    /// # Panics
    /// It could
    /// # Errors
    /// Yes
    pub async fn next(&mut self) -> Result<(), JoinError> {
        while let Some(idx) = self.orphans.pop() {
            self.tasks
                .get_mut(idx)
                .unwrap()
                .task
                .as_mut()
                .unwrap()
                .launch_task();
            self.pending.remove(&idx);
            self.running.insert(idx);
            yield_now().await;
        }

        let running: Vec<_> = self.running.iter().copied().collect();

        for idx in running {
            if self
                .tasks
                .get_mut(idx)
                .unwrap()
                .task
                .as_mut()
                .unwrap()
                .poll_task()
                .await?
                == PollStatus::Finished
            {
                self.running.remove(&idx);
                self.completed.push(idx);

                let children: Vec<_> = self.tasks[idx].children.iter().copied().collect();
                for child_idx in children {
                    self.tasks.get_mut(child_idx).unwrap().parents.remove(&idx);
                    let remove = self.tasks[child_idx].parents.is_empty();
                    if remove {
                        self.orphans.push(child_idx);
                    }
                }
            }
        }
        if !self.running.is_empty() {
            sleep(Duration::from_millis(1)).await;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use crate::{Task, TaskGraph, TaskNode};
    use anyhow::Error;
    use futures::future::lazy;
    use std::thread::sleep;
    use std::time::Duration;
    use tokio::sync::mpsc::channel;
    use tokio::task::{spawn, spawn_blocking};

    #[tokio::test]
    async fn test_2_node() -> Result<(), Error> {
        let mut graph = TaskGraph::new();

        let mut task0 = Task::new(|| Box::pin(lazy(|_| 3 + 1)));
        let mut task1 = Task::new(|| {
            Box::pin(async move {
                spawn_blocking(move || {
                    println!("Got here again");
                    sleep(Duration::from_secs(1));
                    println!("And here");
                    6
                })
                .await
                .unwrap()
            })
        });

        let idx0 = graph
            .push_node(None, TaskNode::from_task(&mut task0))
            .unwrap();
        let idx1 = graph
            .push_node(None, TaskNode::from_task(&mut task1))
            .unwrap();
        graph.attach_child_to_parent(idx0, idx1);

        graph.init();

        while graph.pending.len() > 0 || graph.running.len() > 0 {
            graph.next().await?;
        }

        println!("data0 {:?}", task0.get_data());
        println!("data1 {:?}", task1.get_data());
        Ok(())
    }

    macro_rules! get_mock_task {
        ($id:expr) => {
            Task::new(|| {
                Box::pin(async move {
                    spawn_blocking(move || {
                        let val = rand::random::<u64>() % 1000;
                        println!("random value {} {}", $id, val);
                        sleep(Duration::from_millis(val));
                        ($id, val)
                    })
                    .await
                    .unwrap()
                })
            })
        };
    }

    #[tokio::test]
    async fn test_good_graph() -> Result<(), Error> {
        let mut graph = TaskGraph::new();
        let mut t0 = get_mock_task!("t0");
        let mut t1 = get_mock_task!("t1");
        let mut t2 = get_mock_task!("t2");
        let mut t3 = get_mock_task!("t3");
        let mut t4 = get_mock_task!("t4");
        let mut t5 = get_mock_task!("t5");
        let mut t6 = get_mock_task!("t6");
        let mut t7 = get_mock_task!("t7");

        let n0 = graph.push_node(None, TaskNode::from_task(&mut t0)).unwrap();
        let n1 = graph
            .push_node(Some(n0), TaskNode::from_task(&mut t1))
            .unwrap();

        let n2 = graph
            .push_node(Some(n0), TaskNode::from_task(&mut t2))
            .unwrap();
        let n3 = graph
            .push_node(Some(n0), TaskNode::from_task(&mut t3))
            .unwrap();
        let n4 = graph
            .push_node(Some(n1), TaskNode::from_task(&mut t4))
            .unwrap();
        graph.attach_child_to_parent(n2, n4);
        let _n5 = graph
            .push_node(Some(n3), TaskNode::from_task(&mut t5))
            .unwrap();
        let n6 = graph
            .push_node(Some(n1), TaskNode::from_task(&mut t6))
            .unwrap();
        graph.attach_child_to_parent(n3, n6);
        let n7 = graph
            .push_node(Some(n6), TaskNode::from_task(&mut t7))
            .unwrap();
        graph.attach_child_to_parent(n7, n4);

        graph.init();

        while graph.pending.len() > 0 || graph.running.len() > 0 {
            graph.next().await?;
        }

        for idx in &graph.completed {
            println!(
                "{} {:?}",
                idx,
                graph.get_node_by_index(*idx).unwrap().get_data()
            );
        }
        Ok(())
    }

    #[tokio::test]
    async fn oneshot_test() -> Result<(), Error> {
        let (s01, mut r01) = channel(1);
        let (s02, mut r02) = channel(1);
        let (s03, mut r03) = channel(1);
        let (s14, mut r14) = channel(1);
        let (s16, mut r16) = channel(1);
        let (s24, mut r24) = channel(1);
        let (s36, mut r36) = channel(1);
        let (s35, mut r35) = channel(1);
        let (s46, mut r46) = channel(1);
        let (s67, mut r67) = channel(1);

        let n0 = spawn(async move {
            let val = rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 0 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s01.send(val).await.unwrap();
            s02.send(val).await.unwrap();
            s03.send(val).await.unwrap();
        });
        let n1 = spawn(async move {
            let mut val = r01.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 1 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s14.send(val).await.unwrap();
            s16.send(val).await.unwrap();
        });
        let n2 = spawn(async move {
            let mut val = r02.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 2 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s24.send(val).await.unwrap();
        });
        let n3 = spawn(async move {
            let mut val = r03.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 3 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s35.send(val).await.unwrap();
            s36.send(val).await.unwrap();
        });
        let n4 = spawn(async move {
            let mut val = r14.recv().await.unwrap();
            val += r24.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 4 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s46.send(val).await.unwrap();
        });
        let n5 = spawn(async move {
            let mut val = r35.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 5 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            val
        });
        let n6 = spawn(async move {
            let mut val = r16.recv().await.unwrap();
            val += r36.recv().await.unwrap();
            val += r46.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 6 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            s67.send(val).await.unwrap();
        });
        let n7 = spawn(async move {
            let mut val = r67.recv().await.unwrap();
            val += rand::random::<u64>() % 1000;
            spawn_blocking(move || {
                println!("random value 7 {}", val);
                sleep(Duration::from_millis(val));
            })
            .await
            .unwrap();
            val
        });

        println!("{:?}", n0.await);
        println!("{:?}", n1.await);
        println!("{:?}", n2.await);
        println!("{:?}", n3.await);
        println!("{:?}", n4.await);
        println!("{:?}", n5.await);
        println!("{:?}", n6.await);
        println!("{:?}", n7.await);
        assert!(false);

        Ok(())
    }
}
