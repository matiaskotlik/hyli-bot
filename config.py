import re
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv('DATABASE_URL')

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

FATHER_SONG = '''Father of lies
Cum in disguise
Your cum won't last
There's a snake in my ass
The cum-fathers secret stash
Cum-stomp me flat
I'm going to fuck your dad
Cumming high into the morning sky
Vape cum from my bum til I die
Watching Arthur with a cock in my ass
Riding hard
Eating ass master-class
Sacred cum blade
A fucking crusade
Fatal cum--theft
Give me cum or give me death
Elon's Musk
Jesus Crust
Stealing donations from the Cum-Czar's trust
A cum smoothie gulped smoothly
Consume the cum chalice
Fuck everyone named Alex
David Hayter
Cum Crusader
The Holy Cum Wars
Razor-blade Masturbator
Margaret Thatcher
The Cum Snatcher
Father drowned
Going down on the cum clown
Prolapse pounding
Toothpick sounding
Cum baking
My nipple-pussy is aching
Cum fooler
Semen drooler
Forbidden cum-spice
Your shit-box looks nice!
Life is a cage, and death is the key
All your cum are belong to me
Normalize crying over spilt cum
Making cum-angels with my son
I fucked a fairy in half
How many holes does a human have?
My butt and cunny are in agony
Castration in the sky
Your penis will fly
Scrotal chambers
Semen sailors
Mommy's cum tax
Grind my balls on an axe!
Cum-scented candle
Cum-broiled eggs
Cum-Christ consciousness
Third-eye, cum spy
Cum-scrote sailboat
Semen speed racer
Off-road cum chode
My uterus came out!
Cum treasurer
Dick measurer
Irresponsible Manager of Cum
A cum-slave, back from the grave
The price for breaking a cum-oath
James Hector
Cum key-lector
I tripped in the cum-keeper's crypt
Cum feeder
Moist meter
Sans Undertale, the cum reaper
Fucking a skeleton, right in the pussy
The Dark Souls of cum
Cum-framed, and cum-blamed
Cum-drowning awareness day
Brewing cum-fuel after school
Your nipples are crunchy
The tragic cum-sponge
Your cum is fading...
Sweep up the cum flakes, Joan'''
def filter_line(strg):
    return re.sub(r'[^A-Za-z\n]', '', strg.lower())

FATHER_SONG = FATHER_SONG.splitlines()
FATHER_SONG_FILTERED = [filter_line(line) for line in FATHER_SONG]

ABHISHEK = 315898478712717312
LMAO_PATTERN = re.compile(r'lmf?a+o+', re.IGNORECASE)
ABHI_LMAO = r':lmao:804387193506103316'

# messages
SEND_ERROR = 'The message is too long.'
NO_PERMISSIONS = 'The bot doesn\'t have permissions to do that.'
MESSAGE_TIMER = 3
