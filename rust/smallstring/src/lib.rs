use std::fmt;
use std::ops::Deref;
use std::str::{from_utf8, from_utf8_unchecked, Utf8Error};
use std::string::FromUtf8Error;

const N: usize = 20;

pub enum SmallString {
    Stack { length: usize, buf: [u8; N] },
    Heap(String),
}

impl SmallString {
    /// If input str has length < 20 bytes, copy it to a stack buffer,
    /// otherwise convert it to a string
    pub fn from_str(s: &str) -> SmallString {
        if s.len() < N {
            let mut buf = [0u8; N];
            let length = s.len();
            buf[..length].copy_from_slice(&s.as_bytes()[..length]);
            SmallString::Stack { length, buf }
        } else {
            SmallString::Heap(s.to_string())
        }
    }

    pub fn from_utf8(b: &[u8]) -> Result<SmallString, Utf8Error> {
        let s = from_utf8(b)?;
        Ok(Self::from_str(s))
    }

    pub fn from_string(s: String) -> SmallString {
        SmallString::Heap(s)
    }

    pub fn from_vec(b: Vec<u8>) -> Result<SmallString, FromUtf8Error> {
        String::from_utf8(b).map(|s| Self::from_string(s))
    }

    fn as_str(&self) -> &str {
        match self {
            Self::Stack { length, buf } => unsafe { from_utf8_unchecked(&buf[..*length]) },
            Self::Heap(s) => s.as_str(),
        }
    }
}

impl Deref for SmallString {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        self.as_str()
    }
}

impl fmt::Display for SmallString {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        self.as_str().fmt(f)
    }
}

#[cfg(test)]
mod tests {
    use crate::SmallString;

    #[test]
    fn it_works() {
        let ss = SmallString::from_str("Hello world");
        let s = "Hello world".to_string();
        let ss2 = SmallString::from_string(s);
        println!("{} {}", ss.as_str(), ss2.as_str());
        assert_eq!(*ss, *ss2);
    }
}
