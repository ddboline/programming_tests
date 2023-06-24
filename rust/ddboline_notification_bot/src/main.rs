use anyhow::Error;
use futures::StreamExt;
use std::env;
use telegram_bot::{Api, CanReplySendMessage, MessageKind, UpdateKind};

#[tokio::main]
async fn main() -> Result<(), Error> {
    dotenv::from_filename("config.env").ok();

    let token = env::var("TELEGRAM_BOT_TOKEN").unwrap();
    let api = Api::new(token);

    let mut stream = api.stream();
    while let Some(update) = stream.next().await {
        if let UpdateKind::Message(message) = update?.kind {
            if let MessageKind::Text { ref data, .. } = message.kind {
                // Print received text message to stdout.
                println!("{:?}", message);
                println!("<{}>: {}", &message.from.first_name, data);

                // Answer message with "Hi".
                api.spawn(message.text_reply(format!(
                    "Hi, {}! You just wrote '{}'",
                    &message.from.first_name, data
                )));
            }
        }
    }
    Ok(())
}
