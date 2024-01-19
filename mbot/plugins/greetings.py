"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot,AUTH_CHATS
from os import execvp,sys

@Mbot.on_message(filters.command("start"))
async def start(client,message):
    reply_markup = [[
        InlineKeyboardButton(text="സഹായം",callback_data="helphome"),
        InlineKeyboardButton(text="സ്പോൺസർ",
            url="https://t.me/Drago_Mafia")
        ]]
    if LOG_GROUP:

        invite_link = await client.create_chat_invite_link(chat_id=(int(LOG_GROUP) if str(LOG_GROUP).startswith("-100") else LOG_GROUP))
        reply_markup.append([InlineKeyboardButton("Malayalam Audiobook 📓", url=invite_link.invite_link)])
    if message.chat.type != "private" and message.chat.id not in AUTH_CHATS and message.from_user.id not in SUDO_USERS:
        return await message.reply_text("**നിങ്ങൾക്കിഷ്ടപ്പെട്ട കഥകളുടെ യൂട്യൂബ് ലിങ്കുകൾ എനിക്കയച്ചു തരു,ഞാൻ അവ ഓഡിയോ ക്ലിപ്പുകളായി നൽകാം** 😊.\n\n `ഓഡിയോകൾ` **@malayalam_audiobook** `എന്ന ചാനലിൽ.`",
                    reply_markup=InlineKeyboardMarkup(reply_markup))
    return await message.reply_text(f"**ഹായ്{message.from_user.first_name},**\n\n**വരൂ, യൂട്യൂബ് ഗാനങ്ങൾ സ്വന്തമാക്കാം.നിങ്ങൾക്കിഷ്ടപ്പെട്ട കഥകളുടെ യൂട്യൂബ് ലിങ്കുകൾ എനിക്കയച്ചു തരു,ഞാൻ അവ ഓഡിയോ ക്ലിപ്പുകളായി നൽകാം** 😊.\n\n `ഓഡിയോകൾ` **@malayalam_audiobook** `എന്ന ചാനലിൽ.`",
                    reply_markup=InlineKeyboardMarkup(reply_markup))

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","mbot"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")

@Mbot.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.send(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")

HELP = {

    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
}


@Mbot.on_message(filters.command("help"))
async def help(_,message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]

    await message.reply_text(f"Hello **{message.from_user.first_name}**, I'm **@mp3uploader_bot**.\nI'm Here to download your music.Restart /start \n\n🏅**@signature_98** ",
                        reply_markup=InlineKeyboardMarkup(button))

@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_,query):
    i = query.data.replace("help_","")
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Back",callback_data="helphome")]])
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text = text,reply_markup=button)

@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    await query.message.edit(f"Hello **{query.from_user.first_name}**, I'm **@mp3uploader_bot**.\nI'm Here to download your music.Restart /start \n\n🏅**@signature_98**",
                        reply_markup=InlineKeyboardMarkup(button))
