fn find_min_abs_diff_simple(arr: &[i64]) -> (i64, i64) {
    if arr.len() < 2 {
        panic!("can't continue");
    }
    let mut min_idx = 0;
    let mut max_idx = arr.len() - 1;
    let mut min_sum = None;
    for i in 0..arr.len() {
        let a = arr[i];
        for j in i+1..arr.len() {
            let b = arr[j];
            let (add, overflow) = a.overflowing_add(b);
            if min_sum.is_none() || (!overflow && Some(add.abs()) <= min_sum) {
                min_sum = if overflow {
                    Some(i64::MAX)
                } else {
                    Some(add.abs())
                };
                min_idx = i;
                max_idx = j;
            }
        }
    }
    if arr[min_idx] < arr[max_idx] {
        (arr[min_idx], arr[max_idx])
    } else {
        (arr[max_idx], arr[min_idx])
    }
    
}

fn find_min_abs_diff(arr: &[i64]) -> (i64, i64) {
    if arr.len() < 2 {
        panic!("can't continue");
    }
    let mut v = arr.to_vec();
    v.sort();
    println!("{:?}", v);

    let mut min_idx = 0;
    while min_idx + 1 < v.len() && v[min_idx + 1] < 0 {
        min_idx += 1;
    }

    if min_idx == 0 {
        (v[0], v[1])
    } else if min_idx == v.len() - 1 {
        (v[v.len() - 2], v[v.len() - 1])
    } else {
        let mut max_idx = min_idx + 1;
        let (add, overflow) = v[min_idx].overflowing_add(v[max_idx]);
        if overflow {
            return (v[min_idx], v[max_idx]);
        }
        let mut min_sum = add.abs();

        if min_idx + 2 < v.len() - 1 {
            let (add, overflow) = v[min_idx+1].overflowing_add(v[min_idx+2]);
            if !overflow && add.abs() <= min_sum {
                println!("pos {} {}", v[min_idx+1], v[min_idx+2]);
                min_sum = add.abs();
                min_idx = min_idx + 1;
                max_idx = min_idx + 2;
            }
        }
        if min_idx >= 1 {
            let (add, overflow) = v[min_idx-1].overflowing_add(v[min_idx]);
            if !overflow && add.abs() <= min_sum {
                println!("neg {} {}", v[min_idx-1], v[min_idx]);
                min_sum = add.abs();
                max_idx = min_idx;
                min_idx -= 1;
            }
        }

        let mut left = min_idx;
        loop {
            let mut right = max_idx;
            loop {
                println!("a {} b {}", v[left], v[right]);
                let (add, overflow) = v[left].overflowing_add(v[right]);
                if !overflow && add.abs() <= min_sum {
                    min_idx = left;
                    max_idx = right;
                    min_sum = add.abs();
                }
                if right == v.len() - 1 {
                    break;
                }
                right += 1;
            }
            if left == 0 {
                break;
            }
            left -= 1;
        }

        (v[min_idx], v[max_idx])
    }
}

#[cfg(test)]
mod tests {
    use rand::{thread_rng, Rng};

    use super::{find_min_abs_diff_simple, find_min_abs_diff};

    #[test]
    fn it_works() {
        assert_eq!(find_min_abs_diff(&[5, 4, 3, 1, 8, 10]), (1, 3));
        assert_eq!(find_min_abs_diff(&[-2, -5, -12, -3, -4]), (-3, -2));
        assert_eq!(
            find_min_abs_diff(&[5, -2, -5, 4, 3, 1, 8, 10, -12]),
            (-5, 5)
        );
        assert_eq!(find_min_abs_diff_simple(&[29, -39, 57, 30, -14, 73, -73, -53, 99, -63]), (-73, 73));
        assert_eq!(find_min_abs_diff(&[29, -39, 57, 30, -14, 73, -73, -53, 99, -63]), (-73, 73));
        for _ in 0..20 {
            let arr: Vec<_> = (0..20).map(|_| thread_rng().gen::<i64>() as i64).collect();
            println!("{:?}", arr);
            let simple = find_min_abs_diff_simple(&arr);
            let complex = find_min_abs_diff(&arr);
            assert_eq!(simple, complex);
        }
    }
}
