#[derive(Default)]
struct Trie<T> {
    size: usize,
    root: Node<T>,
}

impl<T> Trie<T> {
    fn len(&self) -> usize {
        self.size
    }

    fn insert<U: AsRef<[u8]>>(&mut self, key: U, value: T) {
        let mut node = &mut self.root;
        for c in key.as_ref() {
            node = node.children.entry(*c).or_default();
        }
        node.value = Some(Arc::new(value));
        self.size += 1;
    }

    fn delete<U: AsRef<[u8]>>(&mut self, key: U) -> (bool, Option<Arc<T>>) {
        fn _delete<T, U: AsRef<[u8]>>(
            node: &mut Node<T>,
            key: U,
            d: usize,
        ) -> (bool, Option<Arc<T>>) {
            let mut value = None;
            if d == key.as_ref().len() {
                value = node.value.take();
                node.value = None;
            } else {
                let c = key.as_ref()[d];
                if let Some(sub_node) = node.children.get_mut(&c) {
                    let (is_empty, remove_value) = _delete(sub_node, key, d + 1);
                    if is_empty {
                        node.children.remove(&c);
                    }
                    if let Some(remove_value) = remove_value {
                        value.replace(remove_value);
                    }
                }
            }
            let is_empty = node.value.is_none() && node.children.is_empty();
            (is_empty, value)
        }
        let (is_empty, value) = _delete(&mut self.root, key, 0);
        if value.is_some() {
            self.size -= 1;
        }
        (is_empty, value)
    }

    fn find_node<U: AsRef<[u8]>>(&self, key: U) -> Option<&Node<T>> {
        let mut node = &self.root;
        for c in key.as_ref() {
            match node.children.get(c) {
                Some(new_node) => {
                    node = new_node;
                }
                None => return None,
            }
        }
        Some(node)
    }

    fn find_node_mut<U: AsRef<[u8]>>(&mut self, key: U) -> Option<&mut Node<T>> {
        let mut node = &mut self.root;
        for c in key.as_ref() {
            match node.children.get_mut(c) {
                Some(new_node) => {
                    node = new_node;
                }
                None => return None,
            }
        }
        Some(node)
    }

    fn find<U: AsRef<[u8]>>(&self, key: U) -> Option<Arc<T>> {
        self.find_node(key).and_then(|node| node.value.clone())
    }

    fn find_mut<U: AsRef<[u8]>>(&mut self, key: U) -> Option<Arc<T>> {
        self.find_node_mut(key).and_then(|node| node.value.clone())
    }

    fn keys_with_prefix<U: AsRef<[u8]>>(&mut self, prefix: &U) -> Vec<Vec<u8>> {
        let mut results = Vec::new();
        if let Some(node) = self.find_node(prefix) {
            node.collect(&mut prefix.as_ref().to_vec(), &mut |prefix, _| {
                results.push(prefix.clone());
            });
        }
        results
    }

    fn values_with_prefix<U: AsRef<[u8]>>(&mut self, prefix: &U) -> Vec<Arc<T>> {
        let mut results = Vec::new();
        if let Some(node) = self.find_node(prefix) {
            node.collect(&mut prefix.as_ref().to_vec(), &mut |_, value| {
                results.push(value.clone());
            });
        }
        results
    }

    fn items_with_prefix<U: AsRef<[u8]>>(&mut self, prefix: &U) -> Vec<(Vec<u8>, Arc<T>)> {
        let mut results = Vec::new();
        if let Some(node) = self.find_node(prefix) {
            node.collect(&mut prefix.as_ref().to_vec(), &mut |prefix, value| {
                results.push((prefix.clone(), value.clone()));
            });
        }
        results
    }
}

struct Node<T> {
    children: BTreeMap<u8, Node<T>>,
    value: Option<Arc<T>>,
}

impl<T> Default for Node<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> Node<T> {
    fn new() -> Self {
        Self {
            children: BTreeMap::new(),
            value: None,
        }
    }

    fn collect<F>(&self, prefix: &mut Vec<u8>, call: &mut F)
    where
        F: FnMut(&Vec<u8>, &Arc<T>),
    {
        if let Some(value) = self.value.as_ref() {
            call(prefix, value);
        }
        for (c, sub_node) in &self.children {
            prefix.push(*c);
            sub_node.collect(prefix, call);
            prefix.pop();
        }
    }
}
