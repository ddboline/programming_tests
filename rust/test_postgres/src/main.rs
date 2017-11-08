extern crate postgres;

use postgres::{Connection, TlsMode};

fn main() {
    let conn = Connection::connect(
        "postgresql://ddboline:BQGIvkKFZPejrKvX@localhost:5432/movie_queue",
        TlsMode::None,
    ).unwrap();

    for row in &conn.query(
        "select show, title, link, rating, source from imdb_ratings where istv is true",
        &[],
    ).unwrap()
    {
        let mut show: String = row.get(0);
        let mut title: String = row.get(1);
        let link: Option<String> = row.get(2);
        let rating: Option<f64> = row.get(3);
        let source: Option<String> = row.get(4);

        let link = link.unwrap_or("".to_string());
        let rating = rating.unwrap_or(-1.0);
        let source = source.unwrap_or("".to_string());

        let rating = if rating < 0.0 { 0.0 } else { rating };

        show.truncate(40);
        title.truncate(40);

        println!(
            "{:40} {:40} {:9} {:1.1} {}",
            show,
            title,
            link,
            rating,
            source
        );
    }
}
