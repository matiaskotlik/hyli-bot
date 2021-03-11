import re
from typing import Optional
import os
from dotenv import load_dotenv
from utils import filter_line

load_dotenv()

GAY1 = 'gay1.jpg'
GAY2 = 'gay2.jpg'
BANGER = 'banger.png'

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

REACTS: list[tuple[Optional[list[int]], re.Pattern, list[str]]] = [
    ([315898478712717312], re.compile(r'\blmf?a+o+\b', re.IGNORECASE), ['<:lmao:804387193506103316>']), # abhishek lmao
    ([229713250793553922], re.compile(r'\bcum(ming)?\b', re.IGNORECASE), ['<:cum:819649767666614303>']), # raghav cum
    ([382674822926434335], re.compile(r'\bmm+\s+penis\b', re.IGNORECASE), ['🤤']), # violet mmm penis
    ([382674822926434335], re.compile(r'\byubee\b', re.IGNORECASE), ['😺', '🐝']), # violet yubee
    ([224292077868023809], re.compile(r'\bju?n?gl?e?\W*(dif|gap)', re.IGNORECASE), ['<:jgdif:818221968297295928>']), # matias jgdif
    ([180439899567030272], re.compile(r'\b(fem)?(boy\s*)?cock\b', re.IGNORECASE), ['🍆']), # zapata eggplant
    (None, re.compile(r'\bsmoger?\b', re.IGNORECASE), [r'<:sadge:753638806460039218>', '🚬']), # smoge
]

MATIAS = 224292077868023809
LEAGUE_ROLE = 554831644557705236
LEAGUE_GIF = 'https://tenor.com/view/squidward-spare-some-change-beggar-gif-13086110'

# messages
SEND_ERROR = 'The message is too long.'
NO_PERMISSIONS = 'This bot is missing permissions to do that.'
MESSAGE_TIMER = 3
