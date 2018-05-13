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

pub fn find_largest_palindrome(limit: u64) -> u64 {
    let mut largest = 0;
    for x in 0..limit {
        for y in 0..limit {
            let z = (limit - x) * (limit - y);
            if number_is_palindrome(z) {
                if z > largest {
                    largest = z;
                }
            }
        }
    }
    largest
}

#[test]
fn test() {
    assert_eq!(find_largest_palindrome(999), 906609);
}
