extern crate rayon;
extern crate rand;

use std::thread;
use std::sync::mpsc;
use std::sync::mpsc::{Sender, Receiver};
use rayon::prelude::*;
use rand::distributions::Range;
use rand::distributions::Sample;
use std::env;

fn work_thread(tx: Sender<String>, idx: usize) {
    let val = format!("Hi from thread {}", idx);

    tx.send(val).unwrap();
}

fn write_thread<T: std::fmt::Display>(rx: Receiver<T>) {
    for received in rx {
        println!("Got: {}", received);
    }
}

fn find_valid_characters(input: &String) -> Vec<char> {
    let mut valid_chars = Vec::new();
    for val in 0..26 {
        valid_chars.push((('A' as u8) + val) as char)
    }
    for val in 0..26 {
        valid_chars.push((('a' as u8) + val) as char)
    }
    valid_chars.sort();
    for ch in input.chars() {
        match valid_chars.binary_search(&ch) {
            Ok(_) => (),
            Err(idx) => valid_chars.insert(idx, ch),
        }
    }
    valid_chars.sort();
    valid_chars
}

fn get_one_time_pad_key(range: usize, keysize: usize) -> Vec<usize> {
    let mut rng = rand::thread_rng();
    let mut otup = Range::new(0, range);
    (0..keysize).map(|_| otup.sample(&mut rng)).collect()
}

struct OneTimePad {
    valid_chars: Vec<char>,
    encrypt_key: Vec<usize>,
}

impl OneTimePad {
    fn new(input: &String) -> OneTimePad {
        let valid_chars_ = find_valid_characters(&input);
        let nchar = valid_chars_.len();
        let keysize = input.len();
        OneTimePad {
            valid_chars: valid_chars_,
            encrypt_key: get_one_time_pad_key(nchar, keysize),
        }
    }

    fn from_key(encrypt_key: &String) -> OneTimePad {
        let valid_chars_ = find_valid_characters(&input);

    }

    fn encrypt_char(&self, chr: char, key: usize) -> char {
        let nchr = self.valid_chars.len();
        match self.valid_chars.binary_search(&chr) {
            Ok(idx) => self.valid_chars[(idx + key) % nchr],
            Err(_) => chr,
        }
    }

    fn encrypt_string(&self, input: &String) -> String {
        input
            .chars()
            .zip(self.encrypt_key.iter())
            .map(|(c, &k)| self.encrypt_char(c, k))
            .collect()
    }

    fn decrypt_string(&self, input: &String) -> String {
        let nchr = self.valid_chars.len();
        let decrypt_key: Vec<usize> = self.encrypt_key.iter().map(|&k| nchr - k).collect();
        input
            .chars()
            .zip(decrypt_key.iter())
            .map(|(c, &k)| self.encrypt_char(c, k))
            .collect()
    }

    fn get_key_str(&self) -> String {
        let key_str: Vec<String> = self.encrypt_key
            .par_iter()
            .map(|&k| (self.valid_chars[k as usize]).to_string())
            .collect();
        key_str.join("")
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

    let vals: Vec<String> = env::args().collect();
    let original = vals.get(1..vals.len()).unwrap().join(" ");

    let one_time_pad = OneTimePad::new(&original);

    let nchr = one_time_pad.valid_chars.len();
    println!(
        "{} {}",
        one_time_pad
            .valid_chars
            .iter()
            .map(|&c| c.to_string())
            .collect::<Vec<String>>()
            .join(""),
        nchr
    );

    let key_str = one_time_pad.get_key_str();

    let encrypted = one_time_pad.encrypt_string(&original);

    let decrypted = one_time_pad.decrypt_string(&encrypted);

    println!("{}\n{}\n{}\n{}", original, key_str, encrypted, decrypted);
}
