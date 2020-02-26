use std::collections::HashSet;
use std::fmt::Debug;
use anyhow::{Error, format_err};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
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
    data: T,
    children: Vec<NodeIndex>,
}

impl<T: Debug> Node<T> {
    pub fn new(data: T) -> Self {
        Self {
            data,
            children: Vec::new(),
        }
    }

    pub fn get_children(&self) -> &[NodeIndex] {
        &self.children
    }
}

pub enum IndexOrData<T> {
    Index(NodeIndex),
    Data(T),
}

#[derive(Debug)]
pub struct GraphVariable<T: Debug> {
    nodes: Vec<Node<T>>,
}

impl<T: Debug> Default for GraphVariable<T> {
    fn default() -> Self {
        Self {nodes: Vec::new()}
    }
}

impl<T: Debug + Eq> GraphVariable<T> {
    pub fn get_node_by_data(&self, data: &T) -> Option<NodeIndex>
    {
        for (idx, node) in self.nodes.iter().enumerate() {
            if &node.data == data {
                return Some(idx.into());
            }
        }
        None
    }
}

impl<T: Debug> GraphVariable<T> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn get_nodes(&self) -> &[Node<T>] {
        &self.nodes
    }

    pub fn get_node_by_index(&self, idx: NodeIndex) -> Option<&Node<T>> {
        self.nodes.get(idx.idx())
    }

    /// Add child to existing node
    pub fn push<U>(
        &mut self,
        parent_index: U,
        index_or_data: IndexOrData<T>,
    ) -> Option<NodeIndex>
    where U: Into<Option<NodeIndex>>
     {
        let parent_index: NodeIndex = match parent_index.into() {
            Some(p) => p,
            None => {
                if let IndexOrData::Data(data) = index_or_data {
                    let child = Node::new(data);
                    let index = self.nodes.len().into();
                    self.nodes.push(child);
                    return Some(index);
                } else {
                    return None;
                }
            }
        };
        if parent_index.idx() < self.nodes.len() {
            let child_index = match index_or_data {
                IndexOrData::Index(index) => index,
                IndexOrData::Data(data) => {
                    let child = Node::new(data);
                    let index = self.nodes.len().into();
                    self.nodes.push(child);
                    index
                }
            };
            let parent = unsafe { self.nodes.get_unchecked_mut(parent_index.idx()) };
            parent.children.push(child_index);
            Some(child_index)
        } else {
            None
        }
    }
}

pub fn kahn_algorithm<T: Debug>(dag: &GraphVariable<T>) -> Result<Vec<NodeIndex>, Error> {
    let mut inverse_graph: Vec<_> = (0..dag.get_nodes().len()).map(|_| HashSet::new()).collect();
    for (idx, node) in dag.get_nodes().iter().enumerate() {
        for children in node.get_children() {
            inverse_graph[children.idx()].insert(idx);
        }
    }
    let dataless_graph: Vec<_> = dag
        .get_nodes()
        .iter()
        .map(|n| n.get_children().to_vec())
        .collect();

    let mut sorted_elements = Vec::new();
    let mut nodes_without_incoming_edge = Vec::new();
    for (idx, parents) in inverse_graph.iter().enumerate() {
        if parents.is_empty() {
            nodes_without_incoming_edge.push(idx);
        }
    }

    while let Some(node_idx) = nodes_without_incoming_edge.pop() {
        sorted_elements.push(node_idx.into());
        for child in &dataless_graph[node_idx] {
            inverse_graph[child.idx()].remove(&node_idx);
            if inverse_graph[child.idx()].is_empty() {
                nodes_without_incoming_edge.push(child.idx());
            }
        }
        println!("{:?}", sorted_elements);
        println!("{:?}", nodes_without_incoming_edge);
        println!("{:?}", inverse_graph);
    }

    for node in &inverse_graph {
        if !node.is_empty() {
            return Err(format_err!("Graph Has Cycles {:?}", inverse_graph));
        }
    }

    Ok(sorted_elements)
}

fn get_good_graph() -> GraphVariable<&'static str> {
    let mut graph = GraphVariable::new();
    let n0 = graph.push(None, IndexOrData::Data("n0")).unwrap();
    let n1 = graph.push(n0, IndexOrData::Data("n1")).unwrap();
    let n2 = graph.push(n0, IndexOrData::Data("n2")).unwrap();
    let n3 = graph.push(n0, IndexOrData::Data("n3")).unwrap();
    let n4 = graph.push(n1, IndexOrData::Data("n4")).unwrap();
    graph.push(n2, IndexOrData::Index(n4)).unwrap();
    graph.push(n3, IndexOrData::Data("n5")).unwrap();
    let n6 = graph.push(n1, IndexOrData::Data("n6")).unwrap();
    graph.push(n3, IndexOrData::Index(n6)).unwrap();
    graph
}

fn get_bad_graph() -> GraphVariable<&'static str> {
    let mut graph = GraphVariable::new();
    let n0 = graph.push(None, IndexOrData::Data("n0")).unwrap();
    let n1 = graph.push(n0, IndexOrData::Data("n1")).unwrap();
    let n2 = graph.push(n0, IndexOrData::Data("n2")).unwrap();
    let n3 = graph.push(n0, IndexOrData::Data("n3")).unwrap();
    let n4 = graph.push(n1, IndexOrData::Data("n4")).unwrap();
    graph.push(n2, IndexOrData::Index(n4)).unwrap();
    graph.push(n3, IndexOrData::Data("n5")).unwrap();
    let n6 = graph.push(n4, IndexOrData::Data("n6")).unwrap();
    graph.push(n3, IndexOrData::Index(n6)).unwrap();
    graph.push(n6, IndexOrData::Index(n1)).unwrap();
    graph
}

fn main() -> Result<(), Error> {
    let graph = get_good_graph();

    let result: Vec<_> = kahn_algorithm(&graph)?.into_iter().map(|i| graph.get_node_by_index(i)).collect();
    println!("{:?}", result);

    let graph = get_bad_graph();
    assert!(kahn_algorithm(&graph).is_err());

    Ok(())
}
