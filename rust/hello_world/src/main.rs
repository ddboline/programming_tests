extern crate rand;

use std::cell::Cell;
use rand::Rng;
// use std::slice::SliceConcatExt;

fn test_fn(x: i32) -> i32{
    x * x + 2
}

fn take(v: Vec<i32>) -> Vec<i32> {
    println!("{}", v[0]);
    v
}

fn join_int_list(l: &Vec<i32>) -> String {
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
        *it = rand::thread_rng().gen_range(1,101)
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
    
    println!("val1 {}", join_int_list(&a));
    
    let b = take(a);
    println!("val2 {}", join_int_list(&b));
    
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
    
    let point = Point { x: 5, y: Cell::new(6) };
    point.y.set(7);
    println!("x: {}, y: {:?}", point.x, point.y);
}
