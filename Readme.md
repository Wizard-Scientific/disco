# disco

Disco is a framework for writing discord bots.
It is based on discord.py but provides some often-used utilities, including:

- help
- frequently asked questions
- bot banter like gm, gn, thanks, etc
- channel usage metrics (requires Postgres)
- response handler framework
- permissions framework
- background asyncio loops
- configuration file
- logging
- "state" as simple data storage in a JSON file (e.g. to track spam)
- dexscreener integration (useful for econ discords)

## Install

```bash
pip install "git+https://github.com/0xidm/disco"
```

## Quickstart

Download the sample configuration files.
There is only one basic task for `.env`, which is to point towards the database and the JSON config file.
The JSON config file supports more data structures, permitting richer configurations.

```bash
wget https://github.com/0xidm/disco/raw/main/docs/env.example -o .env
wget https://github.com/0xidm/disco/raw/main/docs/example.json
basic-disco-bot.py
```

## Postgres support

Disco can track statistics about a channel using Postgres.

```bash
psql -p 5433
create user disco;
create database disco;
grant all privileges on database disco to disco;
```

Update `DB_URI_DISCO` in `.env` so it points to the new database.

Finally, apply database migrations to set up the tables.

```bash
alembic upgrade head
```

## Support for FAQ

Put questions into `usr/faq.json` and update `config.json` so it points to this file.
