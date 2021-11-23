from typing import List
from requests import get
from WallHavenBot import API_KEY, bot, CHANNEL_ID
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError


EMOJI = {
    "heart": "❤️",
    "like": "👍",
    "dislike": "👎"
}

class WallHavenWallpaper:

    def __init__(self, id: str) -> None:
        self.base_path = "https://wallhaven.cc/api/v1/w/"
        self.min_size = 1048576
        self.url = self.base_path + id
        try:
            wall_info = get(self.url)
        except Exception:
            wall_info = None
        if wall_info and str(wall_info.status_code)[0] == "2":
            wall_data = wall_info.json()["data"]
            self.path = wall_data["path"]
            self.thumb = wall_data["thumbs"]["original"]
            self.resolution = wall_data["resolution"]
            self.id = id
            self.size = wall_data["file_size"]
            if not len(wall_data["tags"]) > 1:
                tag = wall_data["tags"][0]
            if len(wall_data["tags"]) > 1:
                tag = wall_data["tags"][1]
            if tag["name"] != "anime":
                self.name = tag["name"]
            if tag["name"] == "anime":
                if tag["alias"] != "":
                    self.name = wall_data["tags"][0]["alias"]
                else:
                    self.name = "Anime"
            self.file_name = f"{self.name} ({self.resolution})"
            if "png" in wall_data["file_type"]:
                self.mime_type = "png"
            if "jpeg" in wall_data["file_type"]:
                self.mime_type = "jpg"
        else:
            self.tags = None
            self.path = None
            self.thumb = None
            self.resolution = None
            self.id = id
            self.size = None
            self.name = None
            self.mime_type = None
        

    def send(self):
        if self.name:
            name = self.name
        if not self.name:
            name = "Anime"
        reply_text = f"{name} (`{self.resolution}`)" + "\n@Not\_Anime\_Wallpapers"
        try:
            bot.send_photo(
                chat_id = CHANNEL_ID,
                photo = self.path,
                caption = reply_text,
                parse_mode = ParseMode.MARKDOWN
            )
            bot.send_document(
                chat_id = CHANNEL_ID,
                document = self.path,
                caption = reply_text,
                parse_mode = ParseMode.MARKDOWN,
                reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text = EMOJI["heart"], 
                        callback_data = f"0:heart"
                    ),
                    InlineKeyboardButton(
                        text = EMOJI["like"], 
                        callback_data = f"0:like"
                    ),
                    InlineKeyboardButton(
                        text = EMOJI["dislike"], 
                        callback_data = f"0:dislike"
                    )
                ]])
            )
        except TelegramError as e:
            print(e)


class WallHavenSearch:

    def __init__(self) -> None:
        self.url = "https://wallhaven.cc/api/v1/search?q=id:1&categories=010&purity=110&sorting=date_added"
        self.per_page = 24
        try:
            wall_search = get(self.url,
                headers = {
                    "X-Api-Key": API_KEY
                }
            )
        except Exception:
            wall_search = None
        if wall_search and wall_search.status_code == 200:
            wall_data = wall_search.json()
            meta = wall_data["meta"]
            self.total = meta["total"]
            self.last_page = meta["last_page"]
            self.current_page = meta["current_page"]
            if self.total > 0:
                wall_list: List[WallHavenWallpaper] = []
                for wall in wall_data["data"]:
                    wall_list.append(WallHavenWallpaper(id = wall["id"]))
                self.wall_list = wall_list
            if self.total == 0:
                self.wall_list = []
        else:
            self.total = 0
            self.last_page = 1
            self.current_page = 1
            self.wall_list = []

