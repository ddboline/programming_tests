use std::collections::HashMap;

pub fn partitions(n: isize) -> isize {
    let mut cache: HashMap<(isize, isize), isize> = HashMap::new();
    partitions_recursive(n, n, &mut cache)
}

fn partitions_recursive(
    n: isize,
    m: isize,
    mut cache: &mut HashMap<(isize, isize), isize>,
) -> isize {
    if let Some(val) = cache.get(&(n, m)) {
        return *val;
    }
    let value = if n == 0 || n == 1 {
        1
    } else if n > m {
        partitions_recursive(m, m, &mut cache)
    } else {
        (0..n).fold(0, |s, i| {
            let largest = n - i;
            s + partitions_recursive(largest, m - largest, &mut cache)
        })
    };
    cache.insert((n, m), value);
    value
}

#[cfg(test)]
mod tests {
    use super::*;

    use rand::Rng;
    use std::collections::HashMap;

    #[test]
    fn test_case_001() {
        assert_eq!(partitions(1), 1);
    }

    #[test]
    fn test_case_002() {
        assert_eq!(partitions(2), 2);
    }

    #[test]
    fn test_case_003() {
        assert_eq!(partitions(3), 3);
    }

    #[test]
    fn test_case_004() {
        assert_eq!(partitions(4), 5);
    }

    #[test]
    fn test_case_005() {
        assert_eq!(partitions(5), 7);
    }

    #[test]
    fn test_case_006() {
        assert_eq!(partitions(6), 11);
    }

    #[test]
    fn test_case_007() {
        assert_eq!(partitions(7), 15);
    }

    #[test]
    fn test_case_010() {
        assert_eq!(partitions(10), 42);
    }

    #[test]
    fn test_case_015() {
        assert_eq!(partitions(15), 176);
    }

    #[test]
    fn test_case_020() {
        assert_eq!(partitions(20), 627);
    }

    #[test]
    fn test_case_030() {
        assert_eq!(partitions(30), 5604);
    }

    #[test]
    fn test_case_050() {
        assert_eq!(partitions(50), 204226);
    }

    #[test]
    fn test_case_100() {
        assert_eq!(partitions(100), 190569292);
    }

    #[test]
    fn test_case_random() {
        fn partitions_for_random_tests(n: isize, h: &mut HashMap<isize, isize>) -> isize {
            if n <= 1 {
                return 1;
            }
            if let Some(size) = h.get(&n) {
                return *size;
            }
            let mut m = n - 1;
            let mut size = 0;
            let mut step = 2;
            while m >= 0 {
                let prev_size = partitions_for_random_tests(m, h);
                size += if (step / 2) % 2 == 1 {
                    prev_size
                } else {
                    prev_size * -1
                };
                m -= if step % 2 == 1 { step } else { step / 2 };
                step += 1;
            }
            h.insert(n, size);
            size
        }

        let mut rng = rand::thread_rng();
        let mut h: HashMap<isize, isize> = HashMap::with_capacity(99);
        for _ in 0..15 {
            let n = 20 + rng.gen::<isize>().abs() % 80;
            let size = partitions_for_random_tests(n, &mut h);
            assert_eq!(partitions(n), size);
        }
    }
}
