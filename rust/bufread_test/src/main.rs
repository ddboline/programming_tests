use std::collections::HashMap;
use std::io::{stdin, BufRead, BufReader};

fn main() {
    let mut counts = HashMap::new();
    let mut buffer = String::new();
    let mut bufread = BufReader::new(stdin());

    loop {
        let bytes_read = bufread.read_line(&mut buffer).unwrap();
        if bytes_read == 0 {
            break;
        }
        for word in buffer.split_whitespace() {
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
