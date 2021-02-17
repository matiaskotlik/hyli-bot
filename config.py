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

ABHISHEK = 315898478712717312
LMAO_PATTERN = re.compile(r'lmf?a+o+', re.IGNORECASE)
ABHI_LMAO = r':lmao:804387193506103316'

# messages
SEND_ERROR = 'The message is too long.'
NO_PERMISSIONS = 'The bot doesn\'t have permissions to do that.'
MESSAGE_TIMER = 3
