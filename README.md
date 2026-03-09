# Invite Tracker Bot

A simple Discord bot that tracks server invites and stores them using SQLite.

## Features

* Tracks who invited whom
* Stores invite data in a database
* Supports scanning old messages
* Detects rejoins and possible alts

## Setup

1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/invite-checker-bot.git
cd invite-tracker-bot
```

2. Install requirements

```
pip install -r requirements.txt
```

3. Run the bot

```
python bot.py
```

## Database

The bot automatically creates `invites.db` to store invite data.

## Note

Do not upload your bot token to GitHub.
