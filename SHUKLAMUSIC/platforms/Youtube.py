import asyncio
import os
import re
import json
import random
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from ..utils.formatters import time_to_seconds
from SHUKLAMUSIC import LOGGER

# =========================
# CONFIG
# =========================

DOWNLOAD_DIR = "downloads"
COOKIE_DIR = "SHUKLAMUSIC/assets/cookies"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# =========================
# COOKIE MANAGER
# =========================

class CookieManager:
    def __init__(self):
        self.cookies = []
        self.checked = False
        self.warned = False

    def get_cookies(self):
        if not self.checked:
            if os.path.isdir(COOKIE_DIR):
                for f in os.listdir(COOKIE_DIR):
                    if f.endswith(".txt"):
                        self.cookies.append(f)
            self.checked = True

        if not self.cookies:
            if not self.warned:
                self.warned = True
                LOGGER("YouTube.py").warning(
                    "YouTube cookies missing → downloads may fail."
                )
            return None

        return os.path.join(COOKIE_DIR, random.choice(self.cookies))


cookie_manager = CookieManager()


# =========================
# yt-dlp DOWNLOAD CORE
# =========================

async def yt_dlp_download(link: str, is_video: bool):
    logger = LOGGER("YouTube.py")

    cookies_file = cookie_manager.get_cookies()

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "merge_output_format": "mkv",
    }

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file
        logger.info(f"🍪 Using cookies: {cookies_file}")

    if is_video:
        ydl_opts["format"] = "bestvideo+bestaudio/best"
    else:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "webm",
            }],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            file_path = ydl.prepare_filename(info)

            if not is_video:
                file_path = os.path.splitext(file_path)[0] + ".webm"

            logger.info(f"✅ Downloaded: {file_path}")
            return file_path

    except Exception as e:
        logger.error(f"❌ yt-dlp failed: {e}")
        return None


# =========================
# PUBLIC DOWNLOAD HELPERS
# =========================

async def download_song(link: str) -> str:
    return await yt_dlp_download(link, is_video=False)


async def download_video(link: str) -> str:
    return await yt_dlp_download(link, is_video=True)


# =========================
# SHELL UTILITY
# =========================

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    return out.decode() if out else err.decode()


# =========================
# YOUTUBE API CLASS
# =========================

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.listbase = "https://youtube.com/playlist?list="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid=False):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message: Message):
        messages = [message]
        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for msg in messages:
            entities = msg.entities or msg.caption_entities
            if not entities:
                continue
            text = msg.text or msg.caption
            for ent in entities:
                if ent.type == MessageEntityType.URL:
                    return text[ent.offset: ent.offset + ent.length]
                if ent.type == MessageEntityType.TEXT_LINK:
                    return ent.url
        return None

    async def details(self, link: str, videoid=False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        r = (await VideosSearch(link, limit=1).next())["result"][0]
        return (
            r["title"],
            r["duration"],
            int(time_to_seconds(r["duration"])) if r["duration"] else 0,
            r["thumbnails"][0]["url"].split("?")[0],
            r["id"],
        )

    async def track(self, link: str, videoid=False):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        r = (await VideosSearch(link, limit=1).next())["result"][0]
        return {
            "title": r["title"],
            "link": r["link"],
            "vidid": r["id"],
            "duration_min": r["duration"],
            "thumb": r["thumbnails"][0]["url"].split("?")[0],
        }, r["id"]

    async def playlist(self, link, limit, user_id, videoid=False):
        if videoid:
            link = self.listbase + link
        link = link.split("&")[0]

        data = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} {link}"
        )
        return [x for x in data.split("\n") if x]

    async def video(self, link: str, videoid=False):
        if videoid:
            link = self.base + link
        file = await download_video(link)
        return (1, file) if file else (0, "Video download failed")

    async def download(
        self,
        link: str,
        mystic,
        video=False,
        videoid=False,
        **kwargs,
    ):
        if videoid:
            link = self.base + link

        file = await download_video(link) if video else await download_song(link)
        return (file, True) if file else (None, False)
