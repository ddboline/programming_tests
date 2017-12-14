fn number_is_palindrome(input: u64) -> bool {
    let mut tmp = input;
    let mut digit_list = Vec::new();
    loop {
        digit_list.push(tmp % 10);
        if tmp < 10 {
            break;
        }
        tmp /= 10;
    }
    let mut reversed = digit_list.clone();
    reversed.reverse();
    digit_list == reversed
}

fn find_largest_palindrome() {
    let mut largest = 0;
    for x in 0..999 {
        for y in 0..999 {
            let z = (999-x) * (999-y);
            if number_is_palindrome(z) {
                if z > largest {
                    largest = z;
                    println!("{} {} {}", (999-x), (999-y), z);
                }
            }
        }
    }
}

fn main() {
    find_largest_palindrome();

    let mut candidate = 4000000;
    'a: loop {
        let mut is_divisible = true;
        'b: for i in 1..21 {
            if candidate % i != 0 {
                is_divisible = false;
                break 'b;
            }
        }
        if is_divisible {
            println!("{} {}", candidate, is_divisible);
            break 'a;
        }
        candidate += 2;
    }
}
