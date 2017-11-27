extern crate futures;
extern crate futures_cpupool;

use futures::Future;
use futures_cpupool::CpuPool;
use std::env;

// checks whether a number is prime, slowly
fn is_prime(num: u64) -> (u64, i64) {
    for i in 2..num {
        if num % i == 0 {
            return (num, i as i64);
        }
    }
    (num, -1)
}

fn main() {
    let vals: Vec<String> = env::args().collect();
    //     let vals = vec![15485867, 1235123123, 5123434123, 3, 177];

    // set up a thread pool
    let pool = CpuPool::new_num_cpus();

    let mut futures = Vec::new();

    for val in vals {
        match String::from(val.clone()).trim().parse::<u64>() {
            Ok(x) => {
                futures.push(pool.spawn_fn(move || {
                    let prime = is_prime(x);
                    let res: Result<(u64, i64), ()> = Ok(prime);
                    res
                }))
            }
            Err(e) => {
                println!("Error {} {}", val, e.to_string());
                ()
            }
        }
    }

    println!("Created the future");
    // unwrap here since we know the result is Ok
    loop {
        let (f, _, next_futures) = futures::future::select_all(futures).wait().unwrap();
        match f {
            (num, -1) => println!("{} Is Prime", num),
            (num, x) => println!("{} Is Divisible by {}", num, x),
        }
        futures = match next_futures.len() {
            0 => break,
            _ => next_futures,
        }
    }
}

#[test]
fn test_main() {
    let vals = vec![15485867, 1235123123, 5123434123, 3, 177];
    let results = vec![-1, 13, 179, -1, 3];

    for (val, res) in vals.into_iter().zip(results.into_iter()) {
        let (_, prime) = is_prime(val);
        assert_eq!(prime, res);
    }
}
