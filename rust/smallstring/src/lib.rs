use std::fmt;
use std::ops::{Deref, DerefMut};
use std::convert::{AsRef, AsMut};
use std::str::{from_utf8, from_utf8_unchecked, from_utf8_unchecked_mut, Utf8Error};
use std::string::FromUtf8Error;

#[cfg(target_pointer_width="64")]
pub const N: usize = 30;
#[cfg(target_pointer_width="32")]
pub const N: usize = 14;

pub enum SmallString {
    Stack {length: u8, buf: [u8;N]},
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
            SmallString::Stack{length: length as u8, buf}
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

    pub fn as_str(&self) -> &str {
        match self {
            Self::Stack{length, buf} => {
                let length = *length as usize;
                unsafe { from_utf8_unchecked(&buf[..length]) }
            }
            Self::Heap(s) => s.as_str(),
        }
    }

    pub fn as_mut_str(&mut self) -> &mut str {
        match self {
            Self::Stack{length, buf} => {
                let length = *length as usize;
                unsafe { from_utf8_unchecked_mut(&mut buf[..length]) }
            }
            Self::Heap(s) => s.as_mut_str(),
        }
    }

    pub fn as_bytes(&self) -> &[u8] {
        match self {
            Self::Stack {length, buf} => {
                let length = *length as usize;
                &buf[..length]
            }
            Self::Heap(s) => s.as_bytes()
        }
    }

    pub fn into_string(self) -> String {
        if let Self::Heap(s) = self {
            s
        } else {
            self.to_string()
        }
    }
}

impl Deref for SmallString {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        self.as_str()
    }
}

impl DerefMut for SmallString {
    fn deref_mut(&mut self) -> &mut Self::Target {
        self.as_mut_str()
    }
}

impl fmt::Display for SmallString {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        self.as_str().fmt(f)
    }
}

impl AsRef<str> for SmallString {
    fn as_ref(&self) -> &str {
        self.as_str()
    }
}

impl AsRef<[u8]> for SmallString {
    fn as_ref(&self) -> &[u8] {
        self.as_bytes()
    }
}

impl AsMut<str> for SmallString {
    fn as_mut(&mut self) -> &mut str {
        self.as_mut_str()
    }
}

#[cfg(test)]
mod tests {
    use std::mem::{align_of_val, size_of_val};

    use crate::SmallString;

    #[test]
    fn it_works() {
        let ss = SmallString::from_str("Hello world");
        let s = "Hello world".to_string();
        let ss2 = SmallString::from_string(s);
        println!("{} {}", ss.as_str(), ss2.as_str());
        assert_eq!(*ss, *ss2);
        assert_eq!(ss.into_string(), "Hello world".to_string());

        let ss = SmallString::from_str("Hello world");
        println!("{} {}", align_of_val(&ss), size_of_val(&ss));
        println!("{} {}", align_of_val(&ss2), size_of_val(&ss2));
        assert_eq!(align_of_val(&ss), 8);
        assert_eq!(size_of_val(&ss), 32);
    }
}
