# Antigravity Telegram Bot

A Telegram bot that serves as a mobile-first work assistant — helping you think, plan, decide, write, and build incrementally from anywhere.

## Features (Planned)

- **Telegram-first workflow** — concise, bullet-point interactions optimized for mobile
- **LLM-powered assistant** — brainstorming, planning, drafting, reviewing, decision support
- **Git pair-programmer** — small-step commits and incremental building

## Quick Start

### Prerequisites

- Python 3.10+
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))

### Setup

```bash
# Clone the repo
git clone https://github.com/tapheret2/antigravity-telegram-bot.git
cd antigravity-telegram-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your bot token

# Run the bot
python -m bot
```

## Project Structure

```
antigravity-telegram-bot/
├── bot/
│   ├── __init__.py        # Package init
│   ├── __main__.py        # Entry point
│   ├── config.py          # Config management
│   ├── handlers/          # Message handlers
│   │   └── __init__.py
│   └── services/          # External service adapters
│       └── __init__.py
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

## License

MIT
