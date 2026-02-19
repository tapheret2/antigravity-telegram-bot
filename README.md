# Antigravity Telegram Bot

A Telegram bot that serves as a mobile-first work assistant — helping you think, plan, decide, write, and build incrementally from anywhere. Powered by **Ollama** (local LLM).

## Features

- **Auto work-mode detection** — brainstorm, plan, draft, review, decide
- **Local LLM** via Ollama — no API keys, no cloud, runs on your machine
- **Telegram-first** — concise, bullet-point interactions optimized for mobile
- **Commands**: `/start`, `/help`, `/mode`

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

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

# Pull an Ollama model (if not already)
ollama pull llama3.2

# Configure environment
cp .env.example .env
# Edit .env with your bot token

# Run the bot
python -m bot
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | — | Bot token from @BotFather |
| `OLLAMA_URL` | ❌ | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | ❌ | `llama3.2` | Model to use |
| `LOG_LEVEL` | ❌ | `INFO` | Logging level |

## Project Structure

```
antigravity-telegram-bot/
├── bot/
│   ├── __init__.py          # Package init
│   ├── __main__.py          # Entry point + commands + error handler
│   ├── config.py            # Settings dataclass (.env loader)
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── router.py        # Auto work-mode detection + routing
│   └── services/
│       ├── __init__.py
│       └── llm.py           # Ollama LLM adapter
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Deployment

### Run as Background Service (Linux)

```bash
# Using systemd
sudo nano /etc/systemd/system/antigravity-bot.service
```

```ini
[Unit]
Description=Antigravity Telegram Bot
After=network.target ollama.service

[Service]
WorkingDirectory=/path/to/antigravity-telegram-bot
ExecStart=/path/to/venv/bin/python -m bot
Restart=always
EnvironmentFile=/path/to/antigravity-telegram-bot/.env

[Install]
WantedBy=multi-user.target
```

### Run on Windows (Task Scheduler or manual)

```powershell
# From project directory with venv activated
python -m bot
```

### Keep Ollama Running

Make sure Ollama is running before starting the bot:
```bash
ollama serve   # if not auto-started
```

## License

MIT
