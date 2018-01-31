use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

const TENDIGIT: u64 = 10000000000;

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
    v: Vec<u64>,
}


impl LargeSum {
    fn new() -> LargeSum {
        LargeSum { v: Vec::new() }
    }

    fn from_string(input: String) -> LargeSum {
        let cap = input.len();
        let v = (0..(cap / 10))
                .map(|idx| {
                    input[(idx * 10)..(idx * 10 + 10)].parse::<u64>().unwrap()
                })
                .collect(),
        }
        v.reverse();
        LargeSum{ v: v }
    }

    fn add(v0: &LargeSum, v1: &LargeSum) -> LargeSum {
        let mut v2 = LargeSum::new();
        idx = 0;
        loop {
            
        }
        
        for idx in 0..5 {
            let jdx = 5 - idx - 1;
            println!("{} {}", idx, jdx);
            let tmp = v0.v[jdx] + v1.v[jdx];
            v2.v[jdx] = tmp % TENDIGIT;
            if jdx + 1 != 5 {
                v2.v[jdx + 1] = tmp / TENDIGIT;
            }
        }
        v2
    }
}

fn large_sum() -> u64 {
    let f = File::open("large_sum.txt").unwrap();
    let b = BufReader::new(f);

    let sum = b.lines().fold(LargeSum::new(), |s, l| {
        let tmp = LargeSum::from_string(l.unwrap());
        println!("{:?}", tmp);
        LargeSum::add_to_sum(&s, &tmp)
    });
    sum.v[0]
}

#[test]
fn test() {
    assert_eq!(find_largest_palindrome(999), 906609);
    assert_eq!(find_largest_divisible(10), 2520);
    assert_eq!(find_largest_divisible(20), 232792560);
    assert_eq!(find_n_prime(6), 13);
    assert_eq!(find_n_prime(10001), 104743);
    assert_eq!(product_of_adjacent_digits(4), 5832);
    assert_eq!(product_of_adjacent_digits(13), 23514624000);
    assert_eq!(special_pyth_triplet().unwrap(), 31875000);
    assert_eq!(sum_of_primes(2000000), 142913828922);
    assert_eq!(largest_product_in_a_grid(), 70600674);
    assert_eq!(triangle_with_n_divisors(500), 76576500);
}

fn main() {
    //     println!(
    //         "find_largest_palindrome(10) {}",
    //         find_largest_palindrome(10)
    //     );
    //     println!("find_largest_divisible(10) {}", find_largest_divisible(10));
    //     println!("find_largest_divisible(20) {}", find_largest_divisible(20));
    //     println!("find_n_prime(6) {}", find_n_prime(6));
    //     println!(
    //         "product_of_adjacent_digits(4) {}",
    //         product_of_adjacent_digits(4)
    //     );
    //     println!("{}", special_pyth_triplet().unwrap());
    //     println!("{}", sum_of_primes(10));
    //     println!("{}", largest_product_in_a_grid());
    //     println!("{:?}", find_number_factors(28));
    //     println!("{}", triangle_with_n_divisors(5));
    println!("large_sum {}", large_sum());
}
