use anyhow::{format_err, Error};
use log::debug;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet, VecDeque};
use std::fmt::Debug;
use std::mem::replace;

#[derive(Clone, Copy, PartialEq, Eq, Debug, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct NodeIndex(usize);

impl NodeIndex {
    pub fn idx(self) -> usize {
        self.0
    }
}

impl From<usize> for NodeIndex {
    fn from(item: usize) -> Self {
        Self(item)
    }
}

#[derive(Debug)]
pub struct Node<T: Debug> {
    data: Option<T>,
    children: BTreeSet<NodeIndex>,
    parents: BTreeSet<NodeIndex>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct NodeSerialize {
    children: BTreeSet<NodeIndex>,
    parent: BTreeSet<NodeIndex>,
}

impl<T: Debug> Node<T> {
    pub fn new(data: T) -> Self {
        Self {
            data: Some(data),
            children: BTreeSet::new(),
            parents: BTreeSet::new(),
        }
    }

    pub fn get_children(&self) -> &BTreeSet<NodeIndex> {
        &self.children
    }

    pub fn get_parents(&self) -> &BTreeSet<NodeIndex> {
        &self.parents
    }
}

impl<T: Debug> Default for Node<T> {
    fn default() -> Self {
        Self {
            data: None,
            children: BTreeSet::new(),
            parents: BTreeSet::new(),
        }
    }
}

pub enum IndexOrData<T> {
    Index(NodeIndex),
    Data(T),
}

#[derive(Debug)]
pub struct Graph<T: Debug> {
    nodes: Vec<Node<T>>,
    occupied: BTreeSet<NodeIndex>,
    free: Vec<NodeIndex>,
}

impl<T: Debug> Default for Graph<T> {
    fn default() -> Self {
        Self {
            nodes: Vec::new(),
            occupied: BTreeSet::new(),
            free: Vec::new(),
        }
    }
}

impl<T: Debug + Eq> Graph<T> {
    pub fn get_node_by_data(&self, data: &T) -> Option<NodeIndex> {
        for idx in &self.occupied {
            let node_data = &self.nodes[idx.idx()];
            if node_data.data.as_ref().unwrap() == data {
                return Some(*idx);
            }
        }
        None
    }
}

impl<T: Debug> Graph<T> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn get_occupied_nodes(&self) -> &BTreeSet<NodeIndex> {
        &self.occupied
    }

    pub fn get_node_by_index(&self, idx: NodeIndex) -> Option<&Node<T>> {
        self.nodes.get(idx.idx())
    }

    fn create_child_in_first_available(&mut self, data: T) -> NodeIndex {
        let child = Node::new(data);
        if let Some(index) = self.free.pop() {
            let node = self.nodes.get_mut(index.idx()).unwrap();
            replace(node, child);
            self.occupied.insert(index);
            index
        } else {
            let index = self.nodes.len().into();
            self.nodes.push(child);
            self.occupied.insert(index);
            index
        }
    }

    pub fn push_index<U>(&mut self, parent_index: U, child_index: NodeIndex) -> Option<NodeIndex>
    where
        U: Into<NodeIndex>,
    {
        let parent_index = parent_index.into();
        if parent_index.idx() < self.nodes.len() {
            let parent = self.nodes.get_mut(parent_index.idx()).unwrap();
            parent.children.insert(child_index);
            let child = self.nodes.get_mut(child_index.idx()).unwrap();
            child.parents.insert(parent_index);
            Some(child_index)
        } else {
            None
        }
    }

    /// Add child to existing node
    pub fn push_child<U>(&mut self, parent_index: U, data: T) -> Option<NodeIndex>
    where
        U: Into<Option<NodeIndex>>,
    {
        let parent_index: NodeIndex = if let Some(p) = parent_index.into() {
            p
        } else {
            return Some(self.create_child_in_first_available(data));
        };
        if parent_index.idx() < self.nodes.len() {
            let child_index = self.create_child_in_first_available(data);
            let parent = self.nodes.get_mut(parent_index.idx()).unwrap();
            parent.children.insert(child_index);
            let child = self.nodes.get_mut(child_index.idx()).unwrap();
            child.parents.insert(parent_index);
            Some(child_index)
        } else {
            None
        }
    }

    pub fn pop(&mut self, index: NodeIndex) -> Option<Node<T>> {
        if !self.occupied.contains(&index) {
            return None;
        }
        let empty_node = Node::default();
        let node = self.nodes.get_mut(index.idx()).unwrap();
        let node = replace(node, empty_node);

        for parent in &node.parents {
            let parent_node = self.nodes.get_mut(parent.idx()).unwrap();
            parent_node.children.remove(&index);
            for child in &node.children {
                parent_node.children.insert(*child);
            }
        }
        for child in &node.children {
            let child_node = self.nodes.get_mut(child.idx()).unwrap();
            child_node.parents.remove(&index);
            for parent in &node.parents {
                child_node.parents.insert(*parent);
            }
        }
        self.occupied.remove(&index);
        self.free.push(index);
        Some(node)
    }
}

pub fn kahn_algorithm<T: Debug>(dag: &Graph<T>) -> Result<Vec<NodeIndex>, Error> {
    let mut parents_graph: BTreeMap<NodeIndex, _> = dag
        .get_occupied_nodes()
        .iter()
        .map(|index| {
            let node = dag.get_node_by_index(*index).expect("No node");
            (*index, node.get_parents().clone())
        })
        .collect();

    let mut sorted_elements = Vec::with_capacity(dag.get_occupied_nodes().len());
    let mut nodes_without_incoming_edge = VecDeque::with_capacity(dag.get_occupied_nodes().len());
    for idx in dag.get_occupied_nodes() {
        let node = dag.get_node_by_index(*idx).expect("Bad index");
        if node.parents.is_empty() {
            nodes_without_incoming_edge.push_back(*idx);
        }
    }

    while let Some(node_idx) = nodes_without_incoming_edge.pop_front() {
        sorted_elements.push(node_idx.into());
        let node = dag.get_node_by_index(node_idx).expect("Bad index");
        for child in node.get_children() {
            let parent_node = parents_graph.get_mut(child).expect("No node");
            parent_node.remove(&node_idx);
            if parent_node.is_empty() {
                nodes_without_incoming_edge.push_back(*child);
            }
        }
        debug!("b {:?}", sorted_elements);
        debug!("c {:?}", nodes_without_incoming_edge);
        debug!("d {:?}", parents_graph);
    }

    for node in parents_graph.values() {
        if !node.is_empty() {
            return Err(format_err!("Graph Has Cycles {:?}", parents_graph));
        }
    }

    Ok(sorted_elements)
}

fn get_good_graph() -> Graph<&'static str> {
    let mut graph = Graph::new();
    let n0 = graph.push_child(None, "n0").unwrap();
    let n1 = graph.push_child(n0, "n1").unwrap();
    let n2 = graph.push_child(n0, "n2").unwrap();
    let n3 = graph.push_child(n0, "n3").unwrap();
    let n4 = graph.push_child(n1, "n4").unwrap();
    graph.push_index(n2, n4).unwrap();
    graph.push_child(n3, "n5").unwrap();
    let n6 = graph.push_child(n1, "n6").unwrap();
    graph.push_index(n3, n6).unwrap();
    let n7 = graph.push_child(n6, "n7").unwrap();
    graph.push_index(n7, n4).unwrap();
    graph
}

fn get_bad_graph() -> Graph<&'static str> {
    let mut graph = Graph::new();
    let n0 = graph.push_child(None, "n0").unwrap();
    let n1 = graph.push_child(n0, "n1").unwrap();
    let n2 = graph.push_child(n0, "n2").unwrap();
    let n3 = graph.push_child(n0, "n3").unwrap();
    let n4 = graph.push_child(n1, "n4").unwrap();
    graph.push_index(n2, n4).unwrap();
    graph.push_child(n3, "n5").unwrap();
    let n6 = graph.push_child(n4, "n6").unwrap();
    graph.push_index(n3, n6).unwrap();
    graph.push_index(n6, n1).unwrap();
    graph
}

fn main() -> Result<(), Error> {
    let graph = get_good_graph();

    let result: Vec<_> = kahn_algorithm(&graph)?
        .into_iter()
        .filter_map(|i| graph.get_node_by_index(i).map(|x| x.data))
        .collect();
    println!("{:?}", result);

    let graph = get_bad_graph();
    assert!(kahn_algorithm(&graph).is_err());

    Ok(())
}
