

from dotenv import load_dotenv
from pathlib import Path
import os
from typing import Optional, Union
import re


def filter_line(strg):
    return re.sub(r'[^A-Za-z\n]', '', strg.lower())


load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
MEDIA_PATH = ROOT_DIR / 'media'

PETPET_TEMPLATE = MEDIA_PATH / 'template.png'
GAY1 = MEDIA_PATH / 'gay1.jpg'
GAY2 = MEDIA_PATH / 'gay2.jpg'
HORNY = MEDIA_PATH / 'horny.gif'
BANGER = MEDIA_PATH / 'banger.png'
MAD = MEDIA_PATH / 'mad.png'
NERD = MEDIA_PATH / 'nerd.png'
SINGLE = MEDIA_PATH / 'single.png'

AMOGUS = MEDIA_PATH / 'amogus.mp3'
YEAH = MEDIA_PATH / 'yeah.mp3'

FATHER_SONG_PATH = MEDIA_PATH / 'fatheroflies.txt'
SHUTUP_PATH = MEDIA_PATH / 'shutup'

HH_SERVER = 401575621819367425
TEST_SERVER = 523240131482877970

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError('Need a discord BOT_TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError('Need a DATABASE_URL')

# discord command prefix
PREFIX = '!'

# uwu channel
UWU_PATTERN = re.compile(r'(uwu|owo)', re.IGNORECASE)

# quotes channel
QUOTES_PATTERN = re.compile(r'^quotes?$', re.IGNORECASE)

# reactions
# REACTION_YES = '✅'
# REACTION_NO = '❌'

with open(FATHER_SONG_PATH, 'r') as fp:
    FATHER_SONG = fp.readlines()


FATHER_SONG = [line.strip() for line in FATHER_SONG]
FATHER_SONG_FILTERED = [filter_line(line) for line in FATHER_SONG]


LFTP = 333707773332291605
LFTP_TRUSTED_ROLE = 618937559996956678

ABHISHEK = 315898478712717312
VIOLET = 382674822926434335
MATIAS = 224292077868023809
RAGHAV = 229713250793553922
ZAPATA = 180439899567030272
LUKE = 160524407016521728
KEVIN = 169935204096409600

LEAGUE_ROLE = 554831644557705236
LEAGUE_GIF = 'https://tenor.com/view/squidward-spare-some-change-beggar-gif-13086110'


# messages
SEND_ERROR = 'The message is too long'
NO_PERMISSIONS = 'This bot is missing permissions to do that'
MESSAGE_TIMER = 3
