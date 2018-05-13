extern crate subprocess;
extern crate failure;

use std::io::{BufReader, BufRead};
use subprocess::Exec;
use failure::Error;

fn combine_pids_proc(v: &[String]) -> Vec<String> {
    let mut pids: Vec<String> = v.get(0..3).unwrap().to_vec();
    let len_v = v.len();
    pids.push(v.get(10..len_v).unwrap().join(" "));
    pids
}


fn main() -> Result<(), Error> {
    let stream_obj = Exec::shell("ps -eF").stream_stdout()?;

    let mut headers = Vec::new();
    let _ = BufReader::new(stream_obj)
        .lines()
        .filter_map(|line| {
            let _tmp = line.unwrap();
            if _tmp.contains("[") {
                return None;
            }
            let items = _tmp.split_whitespace()
                .map(String::from)
                .collect::<Vec<_>>();
            if headers.len() == 0 {
                headers = combine_pids_proc(&items);
                return None;
            }
            let _result = combine_pids_proc(&items);
            if (_result.get(0).unwrap() == "root") | (_result.get(3).unwrap().contains("chrome")) {
                return None;
            }
            let _output = headers.iter().zip(_result.iter());
            let _string = _output
                .map(|(x, y)| format!("{} {}", x, y))
                .collect::<Vec<_>>();
            println!("{}", _string.join(" "));
            Some(_result.clone())
        })
        .collect::<Vec<_>>();
    Ok(())
}
