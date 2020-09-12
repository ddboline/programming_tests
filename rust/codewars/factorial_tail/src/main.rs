use lazy_static::lazy_static;
use std::collections::BTreeMap;

lazy_static! {
    static ref LIST_OF_PRIMES: Vec<usize> = get_primes(256);
}

// fixme
fn zeroes(base: i32, number: i32) -> i32 {
    // let list_of_primes = get_primes();
    let list_of_primes = &LIST_OF_PRIMES;
    let prime_frequency_map = prime_frequency(base, &list_of_primes);
    println!("base {} map {:?}", base, prime_frequency_map);
    let mut lowest_v = None;
    for (k, v) in prime_frequency_map {
        let new_v = legendres_formula(k as usize, number as usize) / v as usize;
        if lowest_v.is_none() {
            lowest_v.replace(new_v);
        } else if Some(new_v) < lowest_v {
            lowest_v.replace(new_v);
        }
    }
    lowest_v.unwrap_or(0) as i32
}

const MAXIMUM_PRIME: usize = 256;

fn get_primes_old() -> Vec<usize> {
    let mut array = [true; MAXIMUM_PRIME];
    array[0] = false;
    array[1] = false;
    for i in 2..=128 {
        for j in 2..=i {
            if i * j < 256 {
                array[i * j] = false;
            }
        }
    }
    (0..256)
        .filter_map(|i| if array[i] { Some(i as usize) } else { None })
        .collect()
}

fn get_primes(max_number: usize) -> Vec<usize> {
    let mut primes = vec![2];
    for candidate in 2..=max_number {
        if !primes.iter().any(|prime| candidate % prime == 0) {
            primes.push(candidate);
        }
    }
    primes
}

fn find_prime_factors(base: usize, list_of_primes: &[usize]) -> Vec<usize> {
    let mut prime_factors = Vec::new();
    let mut current = base;
    while current > 1 {
        for p in list_of_primes {
            if current % *p as usize == 0 {
                prime_factors.push(*p);
                current /= *p as usize;
                break;
            }
        }
    }
    prime_factors.sort();
    prime_factors
}

fn prime_frequency(base: i32, list_of_primes: &[usize]) -> BTreeMap<usize, usize> {
    let prime_factors = find_prime_factors(base as usize, list_of_primes);

    prime_factors
        .into_iter()
        .fold(BTreeMap::new(), |mut bmap, p| {
            *bmap.entry(p).or_default() += 1;
            bmap
        })
}

fn legendres_formula(p: usize, n: usize) -> usize {
    let mut denom = p;
    let mut v = 0;
    while n >= denom {
        v += n / denom;
        denom *= p;
    }
    v
}

fn main() {
    assert_eq!(zeroes(10, 10), 2);
    assert_eq!(zeroes(16, 16), 3);
    assert_eq!(zeroes(21, 3158), 525);
    assert_eq!(zeroes(2, 524288), 524287);

    let primes0 = get_primes_old();
    let primes1 = get_primes(256);

    println!("{:?}", primes0);
    println!("{:?}", primes1);
}
