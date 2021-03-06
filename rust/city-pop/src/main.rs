use anyhow::Error;
use flate2::bufread::GzDecoder;
use serde::Deserialize;
use std::fs::File;
use std::io;
use std::io::{BufRead, BufReader};
use std::path::{Path, PathBuf};
use structopt::StructOpt;
use std::mem;

#[derive(Debug, Deserialize)]
#[serde(rename_all="PascalCase")]
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

fn search<P: AsRef<Path>>(file_path: P, city: &str) -> Result<(), Error> {
    let f = BufReader::new(File::open(file_path)?);
    let gz = GzDecoder::new(f);
    let mut reader = BufReader::new(gz);
    let mut buf = String::new();
    let mut body = String::new();
    while let Ok(n) = reader.read_line(&mut buf) {
        if n == 0 {
            break;
        }
        if body.is_empty() {
            mem::swap(&mut body, &mut buf);
            continue;
        }
        if buf.contains(city) {
            body.push_str(&buf);
        }
        buf.clear();
    }

    let input = io::Cursor::new(body);

    let mut rdr = csv::Reader::from_reader(input);
    let mut sum = 0;

    let total = rdr
        .deserialize::<Row>()
        .filter(|r| r.is_ok())
        .map(|r| r.unwrap())
        .filter(|r| r.population.is_some())
        .filter(|r| r.city.contains(city))
        .map(|r| {
            let pop = r.population.unwrap();
            sum += pop;
            r
        })
        .count();

    println!("{} {}", total, sum);
    Ok(())
}

fn main() -> Result<(), Error> {
    let opts = Options::from_args();
    println!("city {}", opts.city);
    search(&opts.file, &opts.city)
}

#[derive(StructOpt)]
struct Options {
    #[structopt(name = "CITY")]
    city: String,
    #[structopt(short, long)]
    /// Input file
    file: PathBuf,
}
