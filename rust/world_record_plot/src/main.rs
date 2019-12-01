use failure::{err_msg, Error};
use ndarray::Array;
use std::fs::File;
use std::io::{BufRead, BufReader};

const MARATHON_DISTANCE_M: f64 = 42195.0;
const METERS_PER_MILE: f64 = 1609.344;
const MARATHON_DISTANCE_MI: f64 = MARATHON_DISTANCE_M / METERS_PER_MILE;

#[derive(Debug)]
enum WorldRecordValues {
    Header((String, String)),
    Row((f64, f64)),
}

fn main() -> Result<(), Error> {
    let world_records_men: Result<Vec<_>, Error> =
        BufReader::new(File::open("running_world_records_men.txt")?)
            .lines()
            .map(|x| {
                let line = x?;
                let values: Vec<_> = line.split_whitespace().collect();
                if values.is_empty() {
                    return Ok(None);
                }
                if values.len() >= 2 {
                    if let Ok(dist) = values[0].parse::<f64>() {
                        let time: Result<Vec<_>, Error> = values[1]
                            .split(':')
                            .map(|x| x.parse::<f64>().map_err(err_msg))
                            .collect();
                        let time = time?;
                        if time.len() >= 3 {
                            let time = time[0] * 3600. + time[1] * 60. + time[2];
                            println!("{} {:?}", dist, time);
                            Ok(Some(WorldRecordValues::Row((dist, time))))
                        } else {
                            Ok(None)
                        }
                    } else {
                        Ok(Some(WorldRecordValues::Header((
                            values[0].to_string(),
                            values[1].to_string(),
                        ))))
                    }
                } else {
                    Ok(None)
                }
            })
            .filter_map(|x| x.transpose())
            .collect();
    println!("{:?}", world_records_men);
    Ok(())
}
