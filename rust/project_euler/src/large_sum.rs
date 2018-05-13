use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

#[derive(Debug)]
struct LargeSum {
    v: Vec<u8>,
}

impl LargeSum {
    fn new() -> LargeSum {
        LargeSum { v: Vec::new() }
    }

    fn from_string(input: String) -> LargeSum {
        LargeSum {
            v: (0..input.len())
                .map(|idx| input[(idx)..(idx + 1)].parse::<u8>().unwrap())
                .rev()
                .collect(),
        }
    }

    fn get_first_ten_digits(&self) -> String {
        (if self.v.len() < 10 {
             self.v.iter()
         } else {
             self.v
                 .get((self.v.len() - 10)..self.v.len())
                 .unwrap()
                 .iter()
         }).map(|x| x.to_string())
            .rev()
            .collect::<Vec<_>>()
            .join("")
    }

    fn add(&self, v1: &LargeSum) -> LargeSum {
        let mut v2 = LargeSum::new();

        let self_len = self.v.len();
        let v1_len = v1.v.len();

        let len = if self_len > v1_len { self_len } else { v1_len };

        v2.v.resize(len, 0);

        for idx in 0..len {
            let tmp = self.v.get(idx).unwrap_or(&0) + v1.v.get(idx).unwrap_or(&0) +
                v2.v.get(idx).unwrap_or(&0);

            v2.v[idx] = tmp % 10;
            if tmp >= 10 {
                if v2.v.len() < idx + 2 {
                    v2.v.resize(idx + 2, 0);
                }
                v2.v[idx + 1] = tmp / 10;
            }
        }
        v2
    }
}

pub fn large_sum() -> String {
    let f = File::open("large_sum.txt").unwrap();
    let b = BufReader::new(f);

    let sum = b.lines().fold(LargeSum::new(), |s, l| {
        s.add(&LargeSum::from_string(l.unwrap()))
    });
    sum.get_first_ten_digits()
}

#[test]
fn test() {
    assert_eq!(large_sum(), "5537376230");
}
