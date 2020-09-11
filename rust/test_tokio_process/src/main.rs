use anyhow::Error;
use futures::stream::StreamExt;
use std::process::Stdio;
use tokio::io::{AsyncBufRead, AsyncBufReadExt, AsyncRead, AsyncReadExt, AsyncWriteExt, BufReader};
use tokio::process::Command;
use tokio::task::spawn;

#[tokio::main]
async fn main() -> Result<(), Error> {
    // let mut p = Command::new("sh").args(&["temp.sh"])
    //     .kill_on_drop(true)
    //     .stdout(Stdio::piped())
    //     .spawn()?;
    // if let Some(stdout) = p.stdout.as_mut() {
    //     let mut reader = BufReader::new(stdout);
    //     let mut buf = String::new();
    //     while let Ok(bytes) = reader.read_line(&mut buf).await {
    //         if bytes > 0 {
    //             println!("{}", buf);
    //             buf.clear();
    //         }
    //     }
    // }

    let mut p = Command::new("grep")
        .args(&["hello"])
        .kill_on_drop(true)
        .stdout(Stdio::piped())
        .stdin(Stdio::piped())
        .spawn()?;
    let stdin = p.stdin.take();
    let stdout = p.stdout.take();
    if let Some(mut stdin) = stdin {
        stdin.write_all(b"goodbye\n").await?;
        stdin.write_all(b"hello\n").await?;
    }
    if let Some(stdout) = stdout {
        let mut reader = BufReader::new(stdout);
        let mut buf = String::new();
        while let Ok(bytes) = reader.read_line(&mut buf).await {
            if bytes > 0 {
                println!("{}", buf);
                if buf.starts_with("hello") {
                    p.kill()?;
                    break;
                }
                buf.clear();
            }
        }
    }
    println!("Hello, world!");
    Ok(())
}
