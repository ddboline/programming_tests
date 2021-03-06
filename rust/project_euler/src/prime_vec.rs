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

pub fn find_largest_divisible(max_int: u64) -> u64 {
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

pub fn find_n_prime(input: usize) -> u64 {
    let mut primes = PrimeVec::new();
    while primes.primes.len() < input {
        primes.find_next_largest_prime();
    }
    primes.primes[input - 1]
}

pub fn sum_of_primes(input: u64) -> u64 {
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

pub fn find_number_factors(input: u64) -> u64 {
    let mut factors = 0;
    for i in 0..input {
        if input % (i + 1) == 0 {
            factors += 1
        }
    }
    factors
}

pub fn triangle_with_n_divisors(input: u64) -> u64 {
    let mut tidx = 1;
    loop {
        tidx += 1;
        let tval = tidx * (tidx + 1) / 2;
        if find_number_factors(tval) > input {
            return tval;
        }
    }
}

#[test]
fn test() {
    assert_eq!(find_largest_divisible(10), 2520);
    assert_eq!(find_largest_divisible(20), 232792560);
    assert_eq!(find_n_prime(6), 13);
    assert_eq!(find_n_prime(10001), 104743);
    assert_eq!(sum_of_primes(10), 17);
    //     assert_eq!(sum_of_primes(2000000), 142913828922);
    //     assert_eq!(triangle_with_n_divisors(500), 76576500);
    assert_eq!(triangle_with_n_divisors(5), 28);
}
