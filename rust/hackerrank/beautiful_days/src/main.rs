use std::io::stdin;
use std::fs::File;
use std::io::Write;
use std::env::var;

fn beautiful_days(i: i64, j: i64, k: i64) -> i64 {
    (i..=j).filter(|n| {
        is_beautiful(*n, k)
    }).count() as i64
}

fn is_beautiful(n: i64, k: i64) -> bool {
    (n - reverse_number(n)).abs() % k == 0
}

fn reverse_number(n: i64) -> i64 {
    let mut digits = Vec::new();
    let mut number = n;
    while number > 0 {
        digits.push(number % 10);
        number /= 10;
    }
    let mut number = 1;
    let mut total = 0;
    for digit in digits.iter().rev() {
        total += digit * number;
        number *= 10;
    }
    total
}

fn main() {
    let output_path = var("OUTPUT_PATH").unwrap();
    let mut fptr = File::create(&output_path).unwrap();
    let mut buf = String::new();
    stdin().read_line(&mut buf).unwrap();
    let mut ijk = buf.split_whitespace();
    let i: i64 = ijk.next().unwrap().parse().unwrap();
    let j: i64 = ijk.next().unwrap().parse().unwrap();
    let k: i64 = ijk.next().unwrap().parse().unwrap();
    let result = beautiful_days(i, j, k);
    writeln!(fptr, "{}", result).unwrap();
}

#[cfg(test)]
mod tests {
    use super::{reverse_number, beautiful_days};

    #[test]
    fn test() {
        assert_eq!(reverse_number(123456), 654321);
        assert_eq!(beautiful_days(20, 23, 6), 2);
        assert_eq!(beautiful_days(13, 45, 3), 33);
    }
}