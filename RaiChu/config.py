## Coder are here

import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
API_ID = int(getenv("API_ID", "16500893"))
API_HASH = getenv("API_HASH", "82aa13b13db059374b451a2e27594e00")
OWNER_NAME = getenv("OWNER_NAME", "-▶️ᴀꜰᴋ ❛𝗔𝘀𝘁𝘂 [🇮🇳] 𝘅𝗗")
ALIVE_NAME = getenv("ALIVE_NAME", "𝐀𝐒𝐓𝐔")
ASSISTANT_USERNAME = getenv("ASSISTANT_USERNAME", "@Mini_0090")
BOT_USERNAME = getenv("BOT_USERNAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "- ❛𝗠𝗶𝗻𝗮𝘁𝗼 [🇮🇳] 𝘅𝗗")
GROUP_SUPPORT = getenv("GROUP_SUPPORT")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://te.legra.ph/file/37079b16be53e26c79aa2.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Astu00800/RaiChu-MusicV2")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d6f92c979ad96b2031cba.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/be5f551acb116292d15ec.png")
IMG_5 = getenv("IMG_5", "https://telegra.ph/file/c3401a572375b569138c3.png")
IMG_6 = getenv("IMG_6", "https://telegra.ph/file/d8f8fc1de9110b93ca94c.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://te.legra.ph/file/37079b16be53e26c79aa2.jpg")
