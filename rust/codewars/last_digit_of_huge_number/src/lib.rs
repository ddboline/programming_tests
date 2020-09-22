pub fn last_digit(lst: &[u64]) -> u64 {
    match lst.iter().rev().fold(None, |mut last_digits, a| {
        let a = *a;
        if let Some(b) = last_digits {
            let result = last_two_digits(a, b);
            if b == 0 || b == 1 || a == 0 || a == 1 {
                last_digits.replace(result);
            } else {
                let result = if result == 0 || result == 1 {
                    result + 100
                } else {
                    result
                };
                last_digits.replace(result);    
            }
        } else {
            last_digits.replace(a);
        }
        last_digits
    }) {
        Some(x) => x % 10,
        None => 1,
    }

}

pub fn last_digit_old(lst: &[u64]) -> u64 {
    let mut lst = lst.to_vec();
    let mut last_digits = lst.pop();

    while let Some(a) = lst.pop() {
        if let Some(b) = last_digits {
            let result = last_two_digits(a, b);
            if b == 0 || b == 1 || a == 0 || a == 1 {
                last_digits.replace(result);
            } else {
                let result = if result == 0 || result == 1 {
                    result + 100
                } else {
                    result
                };
                last_digits.replace(result);    
            }
        }
    }
    match last_digits {
        Some(x) => x % 10,
        None => 1,
    }
}

fn last_two_digits(x: u64, y: u64) -> u64 {
    if y == 0 {
        1
    } else if y == 1 {
        x % 100
    } else {
        let b = if y % 100 == 0 {
            100
        } else if y % 100 == 1 {
            101
        } else {
            y % 100
        };
        (0..b).fold(1, |result, _| (result * (x % 100)) % 100)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basic_tests() {
        let tests = vec![
            (vec![], 1),
            (vec![0, 0], 1),
            (vec![0, 0, 0], 0),
            (vec![1, 2], 1),
            (vec![3, 4, 5], 1),
            (vec![4, 3, 6], 4),
            (vec![7, 6, 21], 1),
            (vec![12, 30, 21], 6),
            (vec![2, 2, 2, 0], 4),
            (vec![937640, 767456, 981242], 0),
            (vec![123232, 694022, 140249], 6),
            (vec![499942, 898102, 846073], 6),
            (vec![2, 0, 1], 1),
            (vec![2, 2, 1, 2], 4),
        ];

        for test in tests {
            assert_eq!(last_digit(&test.0), test.1);
        }
    }
}
