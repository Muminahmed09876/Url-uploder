# Telegram URL Uploader Bot

A simple Telegram bot to download and upload files from direct links.

## Features
- Upload from any direct downloadable URL
- Custom thumbnail support
- Shows progress bar
- Rename with original filename
- Private message only

## Deployment

### Requirements
- Python 3.9+
- Telegram API ID and HASH: https://my.telegram.org
- Bot Token from @BotFather

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
export API_ID=your_api_id
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token

python bot.py
```

### Deploy to Heroku / Render
- Add config vars: `API_ID`, `API_HASH`, `BOT_TOKEN`
- Deploy using Git or GitHub connected repo
