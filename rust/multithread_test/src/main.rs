use std::thread;
use std::sync::mpsc;
use std::sync::mpsc::{Sender, Receiver};
// use std::time::Duration;

fn work_thread(tx: Sender<String>, idx: usize) {
    let val = format!("Hi from thread {}", idx);

    tx.send(val).unwrap();
}

fn write_thread<T: std::fmt::Display>(rx: Receiver<T>) {
    for received in rx {
        println!("Got: {}", received);
    }
}

fn main() {
    let (tx, rx) = mpsc::channel();

    let mut vals = Vec::new();

    for _ in 0..10 {
        vals.push(tx.clone());
    }
    vals.push(tx);

    for (idx, tx_) in vals.into_iter().enumerate() {
        thread::spawn(move || work_thread(tx_, idx));
    }

    write_thread(rx);
}
