fn main() {
    assert_eq!(&decomp(17), "2^15 * 3^6 * 5^3 * 7^2 * 11 * 13 * 17");
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

fn legendres_formula(p: usize, n: usize) -> usize {
    let mut denom = p;
    let mut v = 0;
    while n >= denom {
        v += n / denom;
        denom *= p;
    }
    v
}

fn decomp(n: i32) -> String {
    if n == 1 {
        return "1".to_string();
    }
    get_primes(n as usize)
        .into_iter()
        .filter_map(|i| match legendres_formula(i as usize, n as usize) {
            0 => None,
            1 => Some(format!("{}", i)),
            vpn => Some(format!("{}^{}", i, vpn)),
        })
        .collect::<Vec<_>>()
        .join(" * ")
}
