extern crate getopts;
extern crate rustc_serialize;
extern crate flate2;
extern crate csv;

use getopts::Options;
use std::env;
use std::fs::File;
use std::path::Path;
use std::io;
// use std::thread;
// use std::error::Error;
// use flate2::read::GzDecoder;

#[derive(Debug, RustcDecodable)]
struct Row {
    country: String,
    city: String,
    accent_city: String,
    region: String,

    // Not every row has data for the population, latitude or longitude!
    // So we express them as `Option` types, which admits the possibility of
    // absence. The CSV parser will fill in the correct value for us.
    population: Option<u64>,
    latitude: Option<f64>,
    longitude: Option<f64>,
}

fn print_usage(program: &str, opts: Options) {
    println!(
        "{}",
        opts.usage(&format!("Usage: {} [options] <city>", program))
    );
}

fn search<P: AsRef<Path>>(file_path: &Option<P>, city: &str) {
    let input: Box<io::Read> = match *file_path {
        None => Box::new(io::stdin()),
        Some(ref file_path) => Box::new(File::open(file_path).unwrap()),
    };

    //     let file = File::open(file_path).unwrap();
    //     let d = GzDecoder::new(&file).unwrap();
    let mut rdr = csv::Reader::from_reader(input);
    let mut sum = 0;

    let total = rdr.decode::<Row>()
        .filter(|r| r.is_ok())
        .map(|r| r.unwrap())
        .filter(|r| r.population.is_some())
        .filter(|r| r.city.contains(city))
        .map(|r| {
            let pop = r.population.unwrap();
            println!("{}, {}: {}", r.city, r.country, pop);
            sum += pop;
            r
        })
        .count();

    println!("{} {}", total, sum);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let program = &args[0];

    let mut opts = Options::new();
    opts.optopt("f", "file", "Input file", "NAME");
    opts.optflag("h", "help", "Show this usage message.");

    let matches = match opts.parse(&args[1..]) {
        Ok(m) => m,
        Err(e) => panic!(e.to_string()),
    };
    if matches.opt_present("h") {
        print_usage(&program, opts);
        return;
    }
    let data_path = matches.opt_str("f");

    let city = if !matches.free.is_empty() {
        &matches.free[0]
    } else {
        print_usage(&program, opts);
        return;
    };

    search(&data_path, city);
}
