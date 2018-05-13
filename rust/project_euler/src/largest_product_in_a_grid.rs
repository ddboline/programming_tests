use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;


pub fn largest_product_in_a_grid() -> u64 {
    let f = File::open("the_number2.txt").unwrap();
    let b = BufReader::new(f);

    let mut grid = Vec::new();
    for line in b.lines() {
        let mut grid_line = Vec::new();
        for c in line.unwrap().split(" ") {
            match c.parse::<u64>() {
                Ok(n) => grid_line.push(n),
                _ => (),
            }
        }
        grid.push(grid_line);
    }
    let mut max_product = 0;
    for idx in 0..(grid.len() - 4) {
        for jdx in 0..(grid[idx].len() - 4) {
            let prods =
                vec![
                    grid[idx][jdx] * grid[idx][jdx + 1] * grid[idx][jdx + 2] * grid[idx][jdx + 3],
                    grid[idx][jdx] * grid[idx + 1][jdx + 1] * grid[idx + 2][jdx + 2] *
                        grid[idx + 3][jdx + 3],
                    grid[idx][jdx] * grid[idx + 1][jdx] * grid[idx + 2][jdx] * grid[idx + 3][jdx],
                    grid[idx][jdx + 3] * grid[idx + 1][jdx + 2] * grid[idx + 2][jdx + 1] *
                        grid[idx + 3][jdx],
                ];
            for prod in prods {
                if prod > max_product {
                    max_product = prod
                }
            }
        }
    }
    max_product
}
