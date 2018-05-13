use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use std::collections::HashSet;

fn number_is_palindrome(input: u64) -> bool {
    let mut tmp = input;
    let mut digit_list = Vec::new();
    loop {
        digit_list.push(tmp % 10);
        if tmp < 10 {
            break;
        }
        tmp /= 10;
    }
    let mut reversed = digit_list.clone();
    reversed.reverse();
    digit_list == reversed
}

fn find_largest_palindrome(limit: u64) -> u64 {
    let mut largest = 0;
    for x in 0..limit {
        for y in 0..limit {
            let z = (limit - x) * (limit - y);
            if number_is_palindrome(z) {
                if z > largest {
                    largest = z;
                }
            }
        }
    }
    largest
}

struct PrimeVec {
    primes: Vec<u64>,
    largest_prime: u64,
}

impl PrimeVec {
    fn new() -> PrimeVec {
        PrimeVec {
            primes: vec![2, 3, 5],
            largest_prime: 5,
        }
    }

    fn add_prime(&mut self, prime: u64) {
        if prime > self.largest_prime {
            self.primes.push(prime);
            self.largest_prime = prime;
        }
    }

    fn find_next_largest_prime(&mut self) -> u64 {
        let mut prime_candidate = self.largest_prime + 2;
        loop {
            let mut i = 0;
            while i < self.primes.len() && prime_candidate % self.primes[i] != 0 {
                i += 1;
            }
            if i == self.primes.len() {
                self.add_prime(prime_candidate);
                break;
            }
            prime_candidate += 2;
        }
        prime_candidate
    }

    fn find_primes_below_max(&mut self, max_int: u64) {
        while self.find_next_largest_prime() < max_int {}
        self.primes.pop();
    }
}

fn find_largest_divisible(max_int: u64) -> u64 {
    let mut primes = PrimeVec::new();
    primes.find_primes_below_max(max_int);
    let largest_common_prime = primes.primes.pop().unwrap();
    let mut candidate = largest_common_prime;

    loop {
        let mut is_divisible = true;
        for i in 1..(max_int + 1) {
            if candidate % i != 0 {
                is_divisible = false;
                break;
            }
        }
        if is_divisible {
            break;
        }
        candidate += largest_common_prime;
    }
    candidate
}

fn find_n_prime(input: usize) -> u64 {
    let mut primes = PrimeVec::new();
    while primes.primes.len() < input {
        primes.find_next_largest_prime();
    }
    primes.primes[input - 1]
}

fn product_of_adjacent_digits(digits: usize) -> u64 {
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

fn special_pyth_triplet() -> Option<usize> {
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

fn sum_of_primes(input: u64) -> u64 {
    let mut primes = PrimeVec::new();
    let mut sum_primes = primes.primes.iter().fold(0, |x, y| x + y);
    loop {
        primes.find_next_largest_prime();
        match primes.largest_prime < input {
            true => sum_primes += primes.largest_prime,
            false => break,
        }
    }
    sum_primes
}

fn largest_product_in_a_grid() -> u64 {
    let f = File::open("the_number2.txt").unwrap();
    let b = BufReader::new(f);

    let mut grid = Vec::new();
    for line in b.lines() {
        let mut grid_line = Vec::new();
        for c in line.unwrap().split(" ") {
            match c.parse::<u64>() {
                Ok(n) => grid_line.push(n),
                _ => (),
            }
        }
        grid.push(grid_line);
    }
    let mut max_product = 0;
    for idx in 0..(grid.len() - 4) {
        for jdx in 0..(grid[idx].len() - 4) {
            let prods =
                vec![
                    grid[idx][jdx] * grid[idx][jdx + 1] * grid[idx][jdx + 2] * grid[idx][jdx + 3],
                    grid[idx][jdx] * grid[idx + 1][jdx + 1] * grid[idx + 2][jdx + 2] *
                        grid[idx + 3][jdx + 3],
                    grid[idx][jdx] * grid[idx + 1][jdx] * grid[idx + 2][jdx] * grid[idx + 3][jdx],
                    grid[idx][jdx + 3] * grid[idx + 1][jdx + 2] * grid[idx + 2][jdx + 1] *
                        grid[idx + 3][jdx],
                ];
            for prod in prods {
                if prod > max_product {
                    max_product = prod
                }
            }
        }
    }
    max_product
}

fn find_number_factors(input: u64) -> u64 {
    let mut factors = 0;
    for i in 0..input {
        if input % (i + 1) == 0 {
            factors += 1
        }
    }
    factors
}

fn triangle_with_n_divisors(input: u64) -> u64 {
    let mut tidx = 1;
    loop {
        tidx += 1;
        let tval = tidx * (tidx + 1) / 2;
        if find_number_factors(tval) > input {
            return tval;
        }
    }
}

#[derive(Debug)]
struct LargeSum {
    v: Vec<u8>,
}


impl LargeSum {
    fn new() -> LargeSum {
        LargeSum { v: Vec::new() }
    }

    fn from_string(input: String) -> LargeSum {
        LargeSum {
            v: (0..input.len())
                .map(|idx| input[(idx)..(idx + 1)].parse::<u8>().unwrap())
                .rev()
                .collect(),
        }
    }

    fn get_first_ten_digits(&self) -> String {
        (if self.v.len() < 10 {
             self.v.iter()
         } else {
             self.v
                 .get((self.v.len() - 10)..self.v.len())
                 .unwrap()
                 .iter()
         }).map(|x| x.to_string())
            .rev()
            .collect::<Vec<_>>()
            .join("")
    }

    fn add(&self, v1: &LargeSum) -> LargeSum {
        let mut v2 = LargeSum::new();

        let self_len = self.v.len();
        let v1_len = v1.v.len();

        let len = if self_len > v1_len { self_len } else { v1_len };

        v2.v.resize(len, 0);

        for idx in 0..len {
            let tmp = self.v.get(idx).unwrap_or(&0) + v1.v.get(idx).unwrap_or(&0) +
                v2.v.get(idx).unwrap_or(&0);

            v2.v[idx] = tmp % 10;
            if tmp >= 10 {
                if v2.v.len() < idx + 2 {
                    v2.v.resize(idx + 2, 0);
                }
                v2.v[idx + 1] = tmp / 10;
            }
        }
        v2
    }
}

fn large_sum() -> String {
    let f = File::open("large_sum.txt").unwrap();
    let b = BufReader::new(f);

    let sum = b.lines().fold(LargeSum::new(), |s, l| {
        s.add(&LargeSum::from_string(l.unwrap()))
    });
    sum.get_first_ten_digits()
}

fn get_next_collatz_element(n: u64) -> u64 {
    match n % 2 {
        0 => n / 2,
        1 => 3 * n + 1,
        _ => panic!("I don't know how this is possible {}", n),
    }
}

fn find_collatz_chain(n: u64) -> Vec<u64> {
    let mut collatz_chain: Vec<u64> = vec![n];
    let mut current_n = n;
    while current_n != 1 {
        current_n = get_next_collatz_element(current_n);
        collatz_chain.push(current_n);
    }
    collatz_chain
}

fn find_longest_chain(largest_n: u64) -> u64 {
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
        current_chain
            .iter()
            .map(|&x| visited_nodes.insert(x.clone()))
            .collect::<Vec<_>>();
    }
    longest_chain_start
}

#[test]
fn test0() {
    assert_eq!(find_largest_palindrome(999), 906609);
    assert_eq!(find_largest_divisible(10), 2520);
    assert_eq!(find_largest_divisible(20), 232792560);
    assert_eq!(find_n_prime(6), 13);
}

#[test]
fn test1() {
    assert_eq!(find_n_prime(10001), 104743);
    assert_eq!(product_of_adjacent_digits(4), 5832);
    assert_eq!(product_of_adjacent_digits(13), 23514624000);
    assert_eq!(special_pyth_triplet().unwrap(), 31875000);
}

#[test]
fn test2() {
    assert_eq!(sum_of_primes(10), 17);
    //     assert_eq!(sum_of_primes(2000000), 142913828922);
    assert_eq!(largest_product_in_a_grid(), 70600674);
    //     assert_eq!(triangle_with_n_divisors(500), 76576500);
    assert_eq!(triangle_with_n_divisors(5), 28);
    assert_eq!(large_sum(), "5537376230");
}

#[test]
fn test3() {
    assert_eq!(find_longest_chain(13), 9);
}

fn main() {
    println!(
        "find_largest_palindrome(10) {}",
        find_largest_palindrome(10)
    );
    println!("find_largest_divisible(10) {}", find_largest_divisible(10));
    println!("find_n_prime(6) {}", find_n_prime(6));
    println!(
        "product_of_adjacent_digits(4) {}",
        product_of_adjacent_digits(4)
    );
    println!("special_pyth_triplet {}", special_pyth_triplet().unwrap());
    println!("sum_of_primes(10) {}", sum_of_primes(10));
    println!("largest_product_in_a_grid {}", largest_product_in_a_grid());
    println!("find_number_factors(28) {}", find_number_factors(28));
    println!(
        "triangle_with_n_divisors(5) {}",
        triangle_with_n_divisors(5)
    );
    println!("large_sum {}", large_sum());
    println!("{:?}", find_longest_chain(1000000));
}
