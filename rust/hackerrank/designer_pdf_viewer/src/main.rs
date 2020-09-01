fn main() {
    let buf = "1 3 1 3 1 4 1 3 2 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5";
    let h: Vec<usize> = buf
        .split_whitespace()
        .map(|i| i.parse().unwrap())
        .collect();
    let buf = "abc";
    assert_eq!(designer_pdf_viewer(&h, &buf), 9);

    let buf = "1 3 1 3 1 4 1 3 2 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 7";
    let h: Vec<usize> = buf
        .split_whitespace()
        .map(|i| i.parse().unwrap())
        .collect();
    let buf = "zaba";
    assert_eq!(designer_pdf_viewer(&h, &buf), 28);
}

fn designer_pdf_viewer(h: &[usize], word: &str) -> usize {
    word.chars().map(|c| {
        let idx = (c as u32 - 'a' as u32) as usize;
        h[idx]
    }).max().unwrap_or(0) * word.len()
}
