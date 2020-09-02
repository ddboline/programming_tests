use anyhow::Error;
use tokio::process::Command;
use tokio::io::{AsyncRead,
    BufReader,
    AsyncBufRead, AsyncBufReadExt,
};
use std::process::Stdio;
use futures::stream::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Error> {
    let mut p = Command::new("sh").args(&["temp.sh"])
        .kill_on_drop(true)
        .stdout(Stdio::piped())
        .spawn()?;
    if let Some(stdout) = p.stdout.as_mut() {
        let mut reader = BufReader::new(stdout);
        let mut buf = String::new();
        while let Ok(bytes) = reader.read_line(&mut buf).await {
            if bytes > 0 {
                println!("{}", buf);
                buf.clear();    
            }
        }
    }
    println!("Hello, world!");
    Ok(())
}
