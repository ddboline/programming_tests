use std::collections::HashSet;

pub fn get_next_collatz_element(n: u64) -> u64 {
    match n % 2 {
        0 => n / 2,
        1 => 3 * n + 1,
        _ => panic!("I don't know how this is possible {}", n),
    }
}

pub fn find_collatz_chain(n: u64) -> Vec<u64> {
    let mut collatz_chain: Vec<u64> = vec![n];
    let mut current_n = n;
    while current_n != 1 {
        current_n = get_next_collatz_element(current_n);
        collatz_chain.push(current_n);
    }
    collatz_chain
}

pub fn find_longest_chain(largest_n: u64) -> u64 {
    let mut longest_chain_length = 0;
    let mut longest_chain_start = 1;
    let mut visited_nodes = HashSet::new();
    for n in 1..(largest_n + 1) {
        if visited_nodes.contains(&n) {
            continue;
        }

        let current_chain = find_collatz_chain(n);
        if current_chain.len() > longest_chain_length {
            longest_chain_length = current_chain.len();
            longest_chain_start = n;
        }
        let _: Vec<_> = current_chain
            .iter()
            .map(|&x| visited_nodes.insert(x.clone()))
            .collect();
    }
    longest_chain_start
}

#[test]
fn test() {
    assert_eq!(find_longest_chain(13), 9);
}
