import re
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# discord command prefix
PREFIX = '!'

# uwu channel
UWU_PATTERN = re.compile('(uwu|owo)', re.IGNORECASE)

# reactions
REACTION_YES = '✅'
REACTION_NO = '❌'

# messages
INVALID_COMMAND = f'{{author}}: Please enter a valid command. Type {PREFIX}help for help.'
NO_PERMISSIONS = '{author}: The bot doesn\'t have permissions to do that.'
MESSAGE_TIMER = 15