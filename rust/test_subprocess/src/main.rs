extern crate subprocess;
extern crate failure;

use std::io::{BufReader, BufRead};
use subprocess::Exec;
use failure::Error;

fn main() -> Result<(), Error> {
    let stream_obj = Exec::shell("ps -eF").stream_stdout()?;
    let bufread_iter = BufReader::new(stream_obj).lines();
    let header = bufread_iter.next();
    for line in bufread_iter.take(10) {
        let items = line.unwrap();
        let items = items.split_whitespace();

        println!(
            "{} {}",
            items.clone().take(3).collect::<Vec<&str>>().join(" "),
            items.clone().last().unwrap()
        );
    }
    //     let test_ps = shell_obj.capture()?.stdout_str();
    //     println!("result {}", test_ps);
    Ok(())
}
