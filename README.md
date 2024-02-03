# Local Monitor Bot

This is a Telegram Bot written in Python 3.10 for scanning local network. Based on aiogram 3.x.

## Features

- Scan local network for router
- Search your local IP
- Search other clients IP
- Send scan results from bot


## Requirements

- pip install python-dotenv
- pip install aiogram
- pip install delegator.py
- pip install scapy

## Usage

- Rename `.env.TMP` to `.env`. Fill environment variables with your data.

```bash
mv .env.TMP .env
```

- Run bot

```bash
python3 main.py
```
