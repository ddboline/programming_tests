use std::io::{stdin, BufRead, BufReader};
use std::collections::HashMap;

fn main() {
    let mut counts = HashMap::new();
    for line_rv in BufReader::new(stdin()).lines() {
        for word in line_rv.unwrap().split_whitespace() {
            *counts.entry(String::from(word)).or_insert(0) += 1;
        }
    }

    let mut items: Vec<_> = counts.into_iter().collect();
    items.sort_by_key(|&(_, count)| -count);

    items = items.into_iter().take(10).collect();
    items.sort_by_key(|&(_, count)| count);

    for (item, count) in items.into_iter() {
        println!("{}: {}", item, count);
    }
}
