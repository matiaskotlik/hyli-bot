# Hyli Bot

General purpose discord bot for me and my friends.

- Runs on Python 3
- Using `discord.py` API wrapper to talk to discord
- `pymongo`/MongoDB is used for some bot functions that use a database
- The python `Pillow` library is used for other bot functions that manipulate images
- `ffmpeg` for some voice related things

# Deployment

The bot itself currently lives in a heroku app that clones from github and restarts itself whenever I push to main, so changes are easy to make.

The database is on MongoDB Atlas. Their free plan has a 512MB limit on the database size and I haven't even hit 100KB yet after years of use.

To run the bot yourself just set the environment variables `DATABASE_URL` and `BOT_TOKEN` (or put them in a .env file in the root of the project) and run `python3 src/main.py`

# Usage:

- install discord voice deps (linux only): `sudo apt install ffmpeg libffi-dev libnacl-dev python3-dev`
- create a virtualenv: `python -m venv venv`
- activate it (linux): `source venv/bin/activate`
- activate it (windows): `venv\Scripts\activate`
- install python dependencies: `pip install -r requirements.txt`