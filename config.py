import re
import os
from dotenv import load_dotenv
from utils import filter_line

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN == None:
    raise ValueError('Need a discord BOT_TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

# discord command prefix
PREFIX = '!'

# uwu channel
UWU_PATTERN = re.compile(r'(uwu|owo)', re.IGNORECASE)

# quotes channel
QUOTES_PATTERN = re.compile(r'^quotes?$', re.IGNORECASE)
NO_QUOTES = 'There aren\'t any quotes right now. Sorry!'

# reactions
# REACTION_YES = '✅'
# REACTION_NO = '❌'




with open('fatheroflies.txt', 'r') as fp:
    FATHER_SONG = fp.readlines()

FATHER_SONG = [line.strip() for line in FATHER_SONG]
FATHER_SONG_FILTERED = [filter_line(line) for line in FATHER_SONG]

ABHISHEK = 315898478712717312
LMAO_PATTERN = re.compile(r'lmf?a+o+', re.IGNORECASE)
ABHI_LMAO = r':lmao:804387193506103316'

MARGARET_PATTERN = re.compile(r'margaret\s+thatcher', re.IGNORECASE)
MARGARET_REACT = '💦'

MATIAS = 224292077868023809
LEAGUE_ROLE = 554831644557705236
LEAGUE_GIF = 'https://tenor.com/view/squidward-spare-some-change-beggar-gif-13086110'

# messages
SEND_ERROR = 'The message is too long.'
NO_PERMISSIONS = 'The bot doesn\'t have permissions to do that.'
MESSAGE_TIMER = 3
