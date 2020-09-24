use std::collections::HashMap;
use std::rc::Rc;

fn part(n: i64) -> String {
    let mut cache: HashMap<(i64, i64), Rc<Vec<i64>>> = HashMap::new();
    let prod = partitions_recursive(n, n, &mut cache);
    let range = prod[prod.len()-1] - prod[0];
    let sum: i64 = prod.iter().sum();
    let mean = sum as f64 / prod.len() as f64;
    let median = median(&prod);
    format!("Range: {} Average: {:.2} Median: {:0.2}", range, mean, median)
}

fn median(arr: &[i64]) -> f64 {
    if arr.is_empty() {
        0.
    } else if arr.len() == 1 {
        arr[0] as f64
    } else if arr.len() % 2 == 1 {
        arr[arr.len() / 2] as f64
    } else {
        let x = arr.len() / 2;
        println!("{:?}, {}", arr, x);
        (arr[x-1] + arr[x]) as f64 / 2.
    }
}

fn partitions_recursive(
    n: i64,
    m: i64,
    mut cache: &mut HashMap<(i64, i64), Rc<Vec<i64>>>,
) -> Rc<Vec<i64>> {
    if let Some(val) = cache.get(&(n, m)) {
        return val.clone();
    }
    let value = if n == 0 || n == 1 {
        Rc::new(vec![1])
    } else if n > m {
        partitions_recursive(m, m, &mut cache)
    } else {
        let mut prod = Vec::new();
        for i in 0..n {
            let largest = n - i;
            let new = partitions_recursive(largest, m - largest, cache);
            for p in new.iter() {
                prod.push(largest * p);
            }
        }
        prod.sort();
        prod.dedup();
        Rc::new(prod)
    };
    cache.insert((n, m), value.clone());
    value
}

#[cfg(test)]
mod tests {
    use super::part;

    fn testequal(ans: &str, sol: &str) {
        assert!(ans == sol, "Expected \"{}\", got \"{}\".", sol, ans);
      }
      
      #[test]
      fn returns_expected() {
            testequal(&part(1), "Range: 0 Average: 1.00 Median: 1.00");
            testequal(&part(2), "Range: 1 Average: 1.50 Median: 1.50");
            testequal(&part(3), "Range: 2 Average: 2.00 Median: 2.00");
            testequal(&part(4), "Range: 3 Average: 2.50 Median: 2.50");
            testequal(&part(5), "Range: 5 Average: 3.50 Median: 3.50");
      }
    }
