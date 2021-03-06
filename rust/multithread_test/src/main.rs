extern crate rayon;
extern crate rand;

use std::thread;
use std::sync::mpsc;
use std::sync::mpsc::{Sender, Receiver};
use rayon::prelude::*;
use rand::distributions::Range;
use rand::distributions::Sample;
use std::env;

fn work_thread(tx: Sender<(String, String, String)>, input: &str) {
    let one_time_pad = OneTimePad::new(&input);

    let key_str = one_time_pad.get_key_str();

    let encrypted = one_time_pad.encrypt_string(&input);

    let decrypted = one_time_pad.decrypt_string(&encrypted);

    tx.send((key_str, encrypted, decrypted)).unwrap();
    thread::sleep(std::time::Duration::from_secs(1));
}

fn write_thread<T: std::fmt::Display>(rx: Receiver<(T, T, T)>) {
    for (key_str, encrypt, decrypt) in rx {
        println!("\nkey:{}\nenc:{}\ndec:{}\n", key_str, encrypt, decrypt);
    }
}

fn get_string(input: &[char]) -> String {
    input
        .par_iter()
        .map(|&c| c.to_string())
        .collect::<Vec<String>>()
        .join("")
}

fn find_valid_characters(input: &str) -> Vec<char> {
    let (a, b): (Vec<_>, Vec<_>) = (0..26)
        .into_par_iter()
        .map(|val| {
            (
                (('A' as u8) + val as u8) as char,
                (('a' as u8) + val as u8) as char,
            )
        })
        .unzip();
    let mut valid_chars: Vec<_> = a.into_par_iter().chain(b.into_par_iter()).collect();
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
    fn new(input: &str) -> OneTimePad {
        let valid_chars_ = find_valid_characters(input);
        let nchar = valid_chars_.len();
        let keysize = input.len();
        OneTimePad {
            valid_chars: valid_chars_,
            encrypt_key: get_one_time_pad_key(nchar, keysize),
        }
    }

    fn decrypt_key(&self) -> Vec<usize> {
        let nchr = self.valid_chars.len();
        self.encrypt_key.par_iter().map(|&k| nchr - k).collect()
    }

    fn encrypt_char(&self, chr: char, key: usize) -> char {
        let nchr = self.valid_chars.len();
        match self.valid_chars.binary_search(&chr) {
            Ok(idx) => self.valid_chars[(idx + key) % nchr],
            Err(_) => chr,
        }
    }

    fn encrypt_string(&self, input: &str) -> String {
        input
            .chars()
            .zip(self.encrypt_key.iter())
            .map(|(c, &k)| self.encrypt_char(c, k))
            .collect()
    }

    fn decrypt_string(&self, input: &str) -> String {
        input
            .chars()
            .zip(self.decrypt_key().iter())
            .map(|(c, &k)| self.encrypt_char(c, k))
            .collect()
    }

    fn get_key_str(&self) -> String {
        get_string(&self.encrypt_key
            .par_iter()
            .map(|&k| self.valid_chars[k as usize])
            .collect::<Vec<char>>())
    }
}

fn main() {
    let exe = env::current_exe().unwrap().display().to_string();

    let original = env::args()
        .into_iter()
        .map(|x| match exe.contains(&x) {
            true => "".to_string(),
            false => x,
        })
        .collect::<Vec<String>>()
        .join(" ");

    let (tx, rx) = mpsc::channel();

    let mut vals = Vec::new();

    for _ in 0..10 {
        vals.push(tx.clone());
    }
    vals.push(tx);

    let _: Vec<_> = vals.into_par_iter()
        .map(|tx_| work_thread(tx_, &original.clone()))
        .collect();

    write_thread(rx);
}
