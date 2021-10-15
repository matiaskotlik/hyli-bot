# Hyli Bot

General purpose discord bot for me and my friends.

- Runs on python3
- Using discord.py API wrapper to talk to discord
- pymongo/MongoDB for some bot functions that use a database
- Pillow for other bot functions that manipulate images
- ffmpeg for some voice related things

# Usage:

- install discord voice deps (linux only): `sudo apt install ffmpeg libffi-dev libnacl-dev python3-dev`
- create a virtualenv: `python -m venv venv`
- activate it (linux): `source venv/bin/activate`
- activate it (windows): `venv\Scripts\activate`
- install python dependencies: `pip install -r requirements.txt`