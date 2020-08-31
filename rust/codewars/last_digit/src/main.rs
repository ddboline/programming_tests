fn main() {
    assert_eq!(last_digit("4", "1"), 4);
    assert_eq!(last_digit("4", "2"), 6);
    assert_eq!(last_digit("9", "7"), 9);
    assert_eq!(last_digit("10", "10000000000"), 0);
    assert_eq!(last_digit("3", "651"), 7);
    assert_eq!(last_digit("1606938044258990275541962092341162602522202993782792835301376","2037035976334486086268445688409378161051468393665936250636140449354381299763336706183397376"), 6);
    assert_eq!(
        last_digit(
            "3715290469715693021198967285016729344580685479654510946723",
            "68819615221552997273737174557165657483427362207517952651"
        ),
        7
    );
}

fn last_digit(str1: &str, str2: &str) -> i32 {
    if str2 == "0" {
        return 1;
    }
    let b: i32 = if str2.len() == 1 {
        str2.parse().unwrap()
    } else if str2.len() >= 2 {
        str2.get(str2.len() - 2..).unwrap().parse().unwrap()
    } else {
        panic!("Invalid input");
    };
    let b = (b % 4) as usize;
    let a: i32 = if str1.len() == 1 {
        str1.parse().unwrap()
    } else {
        str1.get(str1.len() - 1..).unwrap().parse().unwrap()
    };
    match a {
        0 | 1 | 5 | 6 => a,
        4 => {
            if b % 2 == 1 {
                4
            } else {
                6
            }
        }
        9 => {
            if b % 2 == 1 {
                9
            } else {
                1
            }
        }
        2 => {
            let array = [6, 2, 4, 8];
            array[b]
        }
        3 => {
            let array = [1, 3, 9, 7];
            array[b]
        }
        7 => {
            let array = [1, 7, 9, 3];
            array[b]
        }
        8 => {
            let array = [6, 8, 4, 2];
            array[b]
        }
        _ => {
            panic!("Invalid input");
        }
    }
}
