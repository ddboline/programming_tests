extern crate rand;

use std::cell::Cell;
use rand::Rng;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use std::collections::HashMap;
// use std::slice::SliceConcatExt;

fn test_fn(x: i32) -> i32 {
    x * x + 2
}

fn take(v: Vec<i32>) -> Vec<i32> {
    println!("{}", v[0]);
    v
}

fn join_vector<T: ToString>(l: &Vec<T>) -> String {
    let _tmp: Vec<String> = l.iter().map(|x| x.to_string()).collect();
    _tmp.join(",")
}

fn main() {
    let x = 0xab;
    {
        let y = 3;
        println!("x {} y {}", x, y);
    }
    let y = 1.5;

    println!("x {} y {}", test_fn(x), y);

    let f = test_fn;

    println!("x {} x {}", test_fn(x), f(x));

    let x = 82;
    println!("x {}", x);

    let story = "Once upon a time...";

    let ptr = story.as_ptr();
    println!("ptr {:p}", ptr);
    println!("ptr {:p}", &x);

    let mut a: Vec<i32> = vec![0; 20];
    for it in &mut a {
        *it = rand::thread_rng().gen_range(1, 101)
    }

    println!("val {:?}", a);

    let (x, y, z) = (1, 2, 3);
    println!("x {} y {} z {}", x, y, z);

    let x = 5;

    let y = if x == 5 { 10 } else { 15 }; // y: i32
    println!("x {} y {}", x, y);

    let mut x = 5;
    loop {
        x -= 3;
        println!("{}", x);
        if x % 5 == 0 {
            break;
        }
    }
    let mut x = 5;
    let mut done = false;
    while !done {
        x -= 3;
        println!("{}", x);
        if x % 5 == 0 {
            done = true;
        }
    }
    let x = vec![0; 20];
    println!("val0 {:?}", x);

    println!("val1 {}", join_vector(&a));

    let b = take(a);
    println!("val2 {}", join_vector(&b));

    let mut x = 5;
    {
        let y = &mut x;
        *y += 1;
    }
    println!("{}", x);

    let x = 5;
    let y: &i32;
    y = &x;
    println!("{}", y);
    println!("{}", x);

    struct Point {
        x: i32,
        y: Cell<i32>,
    }

    let point = Point {
        x: 5,
        y: Cell::new(6),
    };
    point.y.set(7);
    println!("x: {}, y: {:?}", point.x, point.y);

    struct Circle {
        x: f64,
        y: f64,
        radius: f64,
    }

    impl Circle {
        fn area(&self) -> f64 {
            std::f64::consts::PI * (self.radius * self.radius)
        }

        fn grow(&self, increment: f64) -> Circle {
            Circle {
                x: self.x,
                y: self.y,
                radius: self.radius + increment,
            }
        }

        fn new(x: f64, y: f64, radius: f64) -> Circle {
            Circle {
                x: x,
                y: y,
                radius: radius,
            }
        }
    }

    let c = Circle {
        x: 0.0,
        y: 0.0,
        radius: 2.0,
    };
    println!("{}", c.area());
    let d = c.grow(2.0).area();
    println!("{}", d);

    let values = vec![1, 2, 3, 4];
    for x in &values {
        println!("{}", x);
    }
    let y = values;
    println!("{}", join_vector(&y));

    let c = Circle::new(0.0, 0.0, 2.0);
    println!("{}", c.area());

    let x = Box::new(1);
    let ref y = x;
    println!("{}", y);
    println!("{}", x);
    let x = 2;
    println!("{}", x);

    let a = "hello";
    let b = "world";
    let c = format!("{} {}", a, b);
    println!("{:p} {}", &c, &c.replace(" ", "_"));

    println!("Hello World!");
    let f = File::open("Cargo.toml").unwrap();
    let b = BufReader::new(f);

    for line in b.lines() {
        println!("{}", line.unwrap());
    }

    let mut scores = HashMap::new();

    scores.insert("Blue".to_string(), 10);
    scores.insert("Yellow".to_string(), 50);

    for (k, v) in scores.iter() {
        println!("{} {}", k, v);
    }

    println!("{:?}", scores);

    let teams = vec!["Blue".to_string(), "Yellow".to_string()];
    let initial_scores = vec![10, 50];

    let scores: HashMap<_, _> = teams.into_iter().zip(initial_scores.into_iter()).collect();

    for (k, v) in scores.iter() {
        println!("{} {}", k, v);
    }

    println!("{:?}", scores);

    //     let mut line = String::new();
    //     while b.read_line(&mut line).unwrap() > 0 {
    //         println!("{:p} {}", &line, line.trim());
    //         line.clear()
    //     }
}
