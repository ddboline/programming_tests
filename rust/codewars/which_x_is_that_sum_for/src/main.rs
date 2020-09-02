fn main() {
    println!("{}", u_x(0.5));
}

fn u_x(x: f64) -> f64 {
    let mut total = 0f64;
    let mut power = x;
    let mut index = 1;
    let mut next_term = x;
    while next_term > 1.0e-12 {
        total += next_term;
        power *= x;
        index += 1;
        next_term = index as f64 * power;
    }
    total
}

fn solve(m: f64) -> f64 {
    let mut base = 0.0;
    let mut max = 1.0;
    let mut mid = (max + base) / 2.0;
    let mut value = u_x(mid);
    while (max - base).abs() > 1.0e-12 {
        if (m - value) > 0.0 {
            base = mid;
        } else {
            max = mid;
        }
        mid = (max + base) / 2.0;
        value = u_x(mid);
    }
    mid
}

#[cfg(test)]
    mod tests {
    use super::*;

    fn assert_fuzzy(m: f64, expect: f64) -> () {
      let merr = 1e-12;
      println!("{:?}", m);
      let actual = solve(m);
      println!("Actual {:e}", actual);
      println!("Expect {:e}", expect);
      let inrange = (actual - expect).abs() <= merr;
      if inrange == false {
          println!("Expected value near: {:e} but got: {:e}", actual, expect);
      }
      assert_eq!(inrange, true);
    }
    
    
    #[test]
    fn basic_tests() {
      assert_fuzzy(2.00, 5.000000000000e-01);
      assert_fuzzy(4.00, 6.096117967978e-01);
      assert_fuzzy(5.00, 6.417424305044e-01);
      
    }
}
