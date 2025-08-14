# Telegram Max Bot

This project is a Telegram bot that responds to messages containing the substring "макс" or "max" by sending a random sticker from a specified sticker pack.

## Features

- Listens for messages in a chat.
- Detects the presence of the keywords "макс" or "max".
- Sends a random sticker from a predefined sticker pack in response.

## Requirements

- Python 3.x
- `pyTelegramBotAPI` library

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd telegram-max-bot
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the bot, you need to set up your configuration:

1. Open `src/config.py`.
2. Replace the placeholder values for `BOT_TOKEN` and `STICKER_PACK_ID` with your actual bot token and sticker pack ID.

## Usage

To run the bot, execute the following command:

```
python src/bot.py
```

Make sure your bot is added to the desired chat and has permission to read messages.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.