import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_USERNAME = getenv("OWNER_USERNAME", "icxasta")
BOT_USERNAME = getenv("BOT_USERNAME", "odsmusicbot")
BOT_NAME = getenv("BOT_NAME")

MONGO_DB_URI = getenv("MONGO_DB_URI", None)
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
LOGGER_ID = int(getenv("LOGGER_ID", -1002311769574))
OWNER_ID = int(getenv("OWNER_ID", 5909658683))

PRIVACY_LINK = getenv("PRIVACY_LINK", "https://graph.org/PRIVACY-FOR-TEAM-PURVI-BOTS-09-18")

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ✅ Your working API key inserted here
API_URL = getenv("API_URL", 'https://pytdbotapi.thequickearn.xyz')
VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')
API_KEY = getenv("API_KEY", 'NxGBNexGenBots4e1026')

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Souradipkundu1234/AntaraMusic")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/AntaraUpdates")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/AntaraUpdates")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/fcawaj.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/fcawaj.jpg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
STATS_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/fcawaj.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/fcawaj.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/fcawaj.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://")

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://")
