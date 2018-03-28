#![feature(proc_macro, specialization, const_fn)]
#![feature(const_fn, const_align_of, const_size_of, const_ptr_null, const_ptr_null_mut)]

extern crate pyo3;
extern crate rayon;
extern crate rand;

use rayon::prelude::*;
use rand::distributions::Range;
use rand::distributions::Sample;
use pyo3::prelude::*;


struct OneTimePad {
    valid_chars: Vec<char>,
    encrypt_key: Vec<usize>,
}

impl OneTimePad {
    fn new(keysize: usize, extra_chars: &str) -> OneTimePad {
        let valid_chars_ = find_valid_characters(extra_chars);
        let nchar = valid_chars_.len();
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

fn get_upper_lower_chars() -> Vec<char> {
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
    valid_chars
}

fn find_valid_characters(input: &str) -> Vec<char> {
    let mut valid_chars = get_upper_lower_chars();

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

fn get_string(input: &[char]) -> String {
    input
        .par_iter()
        .map(|&c| c.to_string())
        .collect::<Vec<String>>()
        .join("")
}

#[py::class]
struct PyOneTimePad {
    pad: OneTimePad,
    token: PyToken,
}

#[py::methods]
impl PyOneTimePad {
    #[new]
    fn __new__(obj: &PyRawObject, keysize: usize, input: String) -> PyResult<()> {
        obj.init(|t| {
            PyOneTimePad {
                pad: OneTimePad::new(keysize, &input),
                token: t,
            }
        })
    }

    fn encrypt_string(&self, input: String) -> PyResult<String> {
        Ok(self.pad.encrypt_string(&input))
    }

    fn decrypt_string(&self, _py: Python, input: String) -> PyResult<String> {
        Ok(self.pad.decrypt_string(&input))
    }

    fn get_key_str(&self) -> PyResult<String> {
        Ok(self.pad.get_key_str())
    }
}

#[py::modinit(_one_time_pad)]
fn init_mod(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyOneTimePad>()?;

    Ok(())
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
