from WallHavenBot.api import EMOJI
from WallHavenBot import API_KEY, CHANNEL_ID, updater, dispatcher, bot
from threading import Thread, Event
from time import time
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from WallHavenBot.tracker import PostTracker
from telegram.error import TelegramError
from requests import get

class setInterval:

    def __init__(self, action, interval: int) -> None:
        self.interval = interval
        self.callback = action
        self.stop_event = Event()
        thread = Thread(target = self.__setInterval)
        thread.start()
    
    def __setInterval(self):
        next_time = time() + self.interval
        while not self.stop_event.wait(next_time-time()):
            next_time += self.interval
            self.callback()
    
    def cancel(self):
        self.stop_event.set()


SEARCH_URL = "https://wallhaven.cc/api/v1/search?q=id:1&categories=110&purity=011&sorting=date_added"

def send(post: dict):
    reply_text = "Anime (`{}`)\n@Not\_Anime\_Wallpapers".format(post["resolution"])
    try:
        bot.send_photo(
            chat_id = CHANNEL_ID,
            photo = post["path"],
            caption = reply_text,
            parse_mode = ParseMode.MARKDOWN
        )
        bot.send_document(
            chat_id = CHANNEL_ID,
            document = post["path"],
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


def auto_post():
    tracker = PostTracker()
    latest_post_id = tracker.post_id
    wall_search = get(SEARCH_URL, 
        headers = {
            "X-Api-Key": API_KEY,
            "Cache-Control": "no-cache, private",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }
    )
    if wall_search.status_code == 200:
        wall_list = wall_search.json()["data"]
        posts = []
        if tracker == "":
            posts = wall_list
        if tracker != "":
            _tracker = 24
            for i, wall in enumerate(wall_list):
                if i < _tracker:
                    if wall["id"] != latest_post_id and wall["file_size"] >= 1024*1024:
                        posts.append(wall)
                    if wall["id"] == latest_post_id:
                        _tracker = i
                if i >= _tracker:
                    continue
        posts.reverse()
        if len(posts) > 0:
            print("Loop started")
            for post in posts:
                send(post)
            tracker.update(posts[-1]["id"])
            print("Loop Completed")
        if len(posts) <= 0:
            print("Nothing to post")
    else:
        print(wall_search)


def hearts_likes_dislikes_button(update: Update, context: CallbackContext):
    query = update.callback_query
    msg = update.effective_message
    buttons = msg.reply_markup.inline_keyboard[0]
    data = query.data.split(":")
    heart_text = EMOJI["heart"]
    like_text = EMOJI["like"]
    dislike_text = EMOJI["dislike"]
    new_count = int(data[0]) + 1
    if data[1] == "heart":
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text = f"{heart_text} {new_count}",
                callback_data = f"{new_count}:heart"
            ),
            buttons[1],
            buttons[2]
        ]])
    if data[1] == "like":
        buttons = InlineKeyboardMarkup([[
            buttons[0],
            InlineKeyboardButton(
                text = f"{like_text} {new_count}",
                callback_data = f"{new_count}:like"
            ),
            buttons[2]
        ]])
    if data[1] == "dislike":
        buttons = InlineKeyboardMarkup([[
            buttons[0],
            buttons[1],
            InlineKeyboardButton(
                text = f"{dislike_text} {new_count}",
                callback_data = f"{new_count}:dislike"
            )
        ]])
    try:
        msg.edit_caption(
            caption = msg.caption,
            caption_entities = msg.caption_entities,
            reply_markup = buttons
        )
    except TelegramError as e:
        print(e)



def main():
    print("Starting the instance.")
    dispatcher.add_handler(CallbackQueryHandler(
        hearts_likes_dislikes_button, 
        pattern = r'[0-9]+:(heart|like|dislike)'
    ))
    setInterval(auto_post, 120)
    auto_post()
    updater.start_polling()
    print("Starting the bot...")
    updater.idle()


if __name__ == "__main__":
    main()
