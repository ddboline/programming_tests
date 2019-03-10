extern crate reqwest;

fn main() -> Result<(), reqwest::Error> {
    let mut res = reqwest::get("https://www.rust-lang.org")?.error_for_status()?;

    println!("status {}", res.status());
    println!("headers {}", res.headers());

    let body = res.text()?;
    println!("body {}", body);
    Ok(())
}
