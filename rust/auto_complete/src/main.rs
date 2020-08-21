use auto_complete::trie::Trie;
use std::collections::BTreeMap;
use std::sync::Arc;

fn main() {
    let words = vec!["yash", "neha", "swati", "lakhan", "yasin"];
    let match_str = "ya";

    let mut trie = Trie::default();
    for word in words {
        trie.insert(word, word);
    }
    let results = trie.values_with_prefix(&match_str);
    assert_eq!(results, vec![Arc::new("yash"), Arc::new("yasin")]);

    trie.insert("yaas", "yaas");
    let results = trie.values_with_prefix(&match_str);
    assert_eq!(
        results,
        vec![Arc::new("yaas"), Arc::new("yash"), Arc::new("yasin")]
    );

    println!("{:?}", trie.delete("yaas"));
    let results = trie.values_with_prefix(&match_str);
    assert_eq!(results, vec![Arc::new("yash"), Arc::new("yasin")]);

    assert_eq!(trie.len(), 5);
}
