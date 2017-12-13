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

    fn check_target_number(&self, target_number: &u64, candidate_prime: &u64) -> Option<u64> {
        match target_number % candidate_prime {
            0 => Some(target_number / candidate_prime),
            _ => None,
        }
    }

    fn check_is_existing_prime(&self, target_number: u64) -> bool {
        self.primes.binary_search(&target_number).is_ok()
    }

    fn find_prime_factors(&mut self, input_number: u64) -> Vec<u64> {
        let mut prime_factors = Vec::new();
        let mut target_number = input_number;

        'a: loop {
            for &prime in self.primes.iter() {
                'b: loop {
                    match self.check_target_number(&target_number, &prime) {
                        Some(1) => {
                            prime_factors.push(target_number);
                            break 'a;
                        }
                        Some(new_target) => {
                            prime_factors.push(prime);
                            if self.check_is_existing_prime(new_target) {
                                prime_factors.push(new_target);
                                break 'a;
                            }
                            target_number = new_target;
                        }
                        None => {
                            break 'b;
                        }
                    }
                }
            }
            self.find_next_largest_prime();
            if self.largest_prime * self.largest_prime > target_number {
                prime_factors.push(target_number);
                break 'a;
            }
        }
        prime_factors.sort();
        prime_factors
    }
}

fn main() {
    let test_numbers = vec![
        8675309,
        600851475143,
        615689816516,
        984098498407,
        32135468768,
    ];
    let mut primes = PrimeVec::new();
    for test_n in test_numbers {
        let prime_factors = primes.find_prime_factors(test_n);
        let product = prime_factors.iter().fold(1, |a, b| a * b);
        println!(
            "{:?} {} {} {}",
            prime_factors,
            primes.largest_prime,
            test_n,
            product
        );
    }
}
