fn main() {
    assert_eq!(zeros(0), 0);
    assert_eq!(zeros(6), 1);
    assert_eq!(zeros(14), 2);
    assert_eq!(zeros(30), 7);
    assert_eq!(zeros(1000), 249);
    assert_eq!(zeros(100000), 24999);
    assert_eq!(zeros(1000000000), 249999998);
}

fn zeros(n: u64) -> u64 {
    let mut num_zeros = 0;
    let mut denom = 5;
    while n > denom {
        num_zeros += n / denom;
        denom *= 5;
    }
    num_zeros
}
