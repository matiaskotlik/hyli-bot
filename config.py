import re
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = os.getenv("BOT_TOKEN")

# discord command prefix
PREFIX = '!'

# uwu channel
UWU_PATTERN = re.compile('(uwu|owo)', re.IGNORECASE)

# reactions
# REACTION_YES = '✅'
# REACTION_NO = '❌'

ABHISHEK = 315898478712717312
ABHI_LMAO = r':lmao:804387193506103316'

# messages
# INVALID_COMMAND = f'{{author}}: That\'s not a valid command.'
SEND_ERROR = '{author}: The message is too long.'
NO_PERMISSIONS = '{author}: The bot doesn\'t have permissions to do that.'
# MESSAGE_TIMER = 15
