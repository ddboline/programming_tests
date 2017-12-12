extern crate rayon;
extern crate futures;
extern crate futures_cpupool;

use futures::Future;
use futures_cpupool::CpuPool;
use std::sync::Arc;
use std::path::Path;
use std::fs::File;
use std::io::{BufReader, BufRead};
use rayon::prelude::*;
use std::cmp;

static NUM_CHUNKS: usize = 32;

struct LabelPixel {
    label: i32,
    pixels: Vec<i32>,
}


fn slurp_file(file: &Path) -> Vec<LabelPixel> {
    BufReader::new(File::open(file).unwrap())
        .lines()
        .skip(1)
        .map(|line| {
            let line = line.unwrap();
            let mut iter = line.trim().split(',').map(|x| x.parse::<i32>().unwrap());

            LabelPixel {
                label: iter.next().unwrap(),
                pixels: iter.collect(),
            }
        })
        .collect()
}

fn distance_sqr(x: &[i32], y: &[i32]) -> i32 {
    // run through the two vectors, summing up the squares of the differences
    x.iter().zip(y.iter()).fold(
        0,
        |s, (&a, &b)| s + (a - b) * (a - b),
    )
}

fn classify(training: &[LabelPixel], pixels: &[i32]) -> i32 {
    training
        .iter()
        // find element of `training` with the smallest distance_sqr to `pixel`
        .min_by(|p, q| {
            distance_sqr(p.pixels.as_slice(), pixels)
            .cmp(&distance_sqr(q.pixels.as_slice(), pixels))}).unwrap()
        .label
}

fn main_no_par() {
    let training_set = slurp_file(&Path::new("trainingsample.csv"));
    let validation_sample = slurp_file(&Path::new("validationsample.csv"));

    let num_correct = validation_sample
        .par_iter()
        .filter(|x| {
            classify(training_set.as_slice(), x.pixels.as_slice()) == x.label
        })
        .count();

    println!(
        "Percentage correct: {}%",
        num_correct as f64 / validation_sample.len() as f64 * 100.0
    );
}

fn main() {
    // "atomic reference counted": guaranteed thread-safe shared
    // memory. The type signature and API of `Arc` guarantees that
    // concurrent access to the contents will be safe, due to the `Share`
    // trait.
    let training_set = Arc::new(slurp_file(&Path::new("trainingsample.csv")));
    let validation_sample = Arc::new(slurp_file(&Path::new("validationsample.csv")));

    let chunk_size = (validation_sample.len() + NUM_CHUNKS - 1) / NUM_CHUNKS;

    let pool = CpuPool::new_num_cpus();

    let mut futures = Vec::new();

    for i in 0..NUM_CHUNKS {
        // create new "copies" (just incrementing the reference
        // counts) for our new future to handle.
        let ts = training_set.clone();
        let vs = validation_sample.clone();

        futures.push(pool.spawn_fn(move || {
            // compute the region of the vector we are handling...
            let lo = i * chunk_size;
            let hi = cmp::min(lo + chunk_size, vs.len());

            // ... and then handle that region.
            let result: Result<usize, ()> = Ok(
                vs.as_slice()
                    .get(lo..hi)
                    .unwrap()
                    .iter()
                    .filter(|x| classify(ts.as_slice(), x.pixels.as_slice()) == x.label)
                    .count()
            );
            result
        }))
    }

    // run through the futures (waiting for each to complete) and sum the results

    let mut results = Vec::new();
    loop {
        let (f, _, next_futures) = futures::future::select_all(futures).wait().unwrap();
        results.push(f);
        futures = match next_futures.len() {
            0 => break,
            _ => next_futures,
        }
    }


    let num_correct = results.into_iter().fold(0, |a, b| a + b);

    println!(
        "Percentage correct: {}%",
        num_correct as f64 / validation_sample.len() as f64 * 100.0
    );
}
