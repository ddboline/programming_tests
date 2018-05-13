use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

pub fn product_of_adjacent_digits(digits: usize) -> u64 {
    let f = File::open("the_number.txt").unwrap();
    let b = BufReader::new(f);

    let mut the_number = Vec::new();
    for line in b.lines() {
        for c in line.unwrap().chars() {
            match c.to_digit(10) {
                Some(n) => the_number.push(n as u64),
                _ => (),
            };
        }
    }
    let mut max_product = 0;
    for idx in 0..(the_number.len() - digits) {
        let current_product = the_number[idx..(idx + digits)].iter().fold(1, |x, y| x * y);
        if current_product > max_product {
            max_product = current_product
        }
    }
    max_product
}

pub fn special_pyth_triplet() -> Option<usize> {
    let mut list_of_squares = Vec::new();
    for idx in 1..1000 {
        list_of_squares.push(idx * idx);
    }
    for idx in 0..list_of_squares.len() {
        for jdx in idx..list_of_squares.len() {
            let sumsquares = list_of_squares[idx] + list_of_squares[jdx];
            match list_of_squares.binary_search(&sumsquares) {
                Ok(kdx) => {
                    if idx + jdx + kdx + 3 == 1000 {
                        return Some((idx + 1) * (jdx + 1) * (kdx + 1));
                    }
                }
                Err(_) => (),
            }
        }
    }
    None
}
