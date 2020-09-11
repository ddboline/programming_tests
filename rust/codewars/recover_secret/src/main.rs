use std::collections::{HashMap, HashSet};

fn recover_secret(triplets: Vec<[char; 3]>) -> String {
    let mut h: HashMap<_, HashSet<_>> =
        triplets.into_iter().fold(HashMap::new(), |mut h, triplet| {
            for i in 0..3 {
                let s = h.entry(triplet[i]).or_insert_with(|| HashSet::new());
                for j in i + 1..3 {
                    s.insert(triplet[j]);
                }
            }
            h
        });
    let mut chars = Vec::new();
    while !h.is_empty() {
        if let Some(to_remove) = h
            .iter()
            .find_map(|(k, v)| if v.is_empty() { Some(*k) } else { None })
        {
            chars.push(to_remove);
            h.remove(&to_remove);
            for v in h.values_mut() {
                v.remove(&to_remove);
            }
        } else {
            unreachable!();
        }
    }
    chars.into_iter().rev().collect()
}

fn main() {
    println!("Hello, world!");
}

#[test]
fn example_test() {
    assert_eq!(
        recover_secret(vec![
            ['t', 'u', 'p'],
            ['w', 'h', 'i'],
            ['t', 's', 'u'],
            ['a', 't', 's'],
            ['h', 'a', 'p'],
            ['t', 'i', 's'],
            ['w', 'h', 's']
        ]),
        "whatisup"
    );
}
