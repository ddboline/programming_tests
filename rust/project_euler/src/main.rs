pub mod palindrome;
pub mod prime_vec;
pub mod digits_triplets;
pub mod largest_product_in_a_grid;
pub mod large_sum;
pub mod collatz_chain;

use palindrome::find_largest_palindrome;
use prime_vec::{sum_of_primes, find_largest_divisible, find_n_prime, find_number_factors,
                triangle_with_n_divisors};
use digits_triplets::{product_of_adjacent_digits, special_pyth_triplet};
use largest_product_in_a_grid::largest_product_in_a_grid;
use large_sum::large_sum;
use collatz_chain::find_longest_chain;

fn main() {
    println!(
        "find_largest_palindrome(10) {}",
        find_largest_palindrome(10)
    );
    println!("find_largest_divisible(10) {}", find_largest_divisible(10));
    println!("find_n_prime(6) {}", find_n_prime(6));
    println!(
        "product_of_adjacent_digits(4) {}",
        product_of_adjacent_digits(4)
    );
    println!("special_pyth_triplet {}", special_pyth_triplet().unwrap());
    println!("sum_of_primes(10) {}", sum_of_primes(10));
    println!("largest_product_in_a_grid {}", largest_product_in_a_grid());
    println!("find_number_factors(28) {}", find_number_factors(28));
    println!(
        "triangle_with_n_divisors(5) {}",
        triangle_with_n_divisors(5)
    );
    println!("large_sum {}", large_sum());
    println!("find_longest_chain(1000) {}", find_longest_chain(1000));
}
