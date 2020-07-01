import html
import random
import re
import urllib.request
import urllib.parse
import time

from datetime import datetime
from typing import Optional, List

import requests
import wikipedia

from random import randint
from PyLyrics import *
from pythonping import ping as ping3
from requests import get
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from hitsuki import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS
from hitsuki.__main__ import STATS, USER_INFO, GDPR
from hitsuki.modules.disable import DisableAbleCommandHandler
from hitsuki.modules.helper_funcs.extraction import extract_user
from hitsuki.modules.helper_funcs.filters import CustomFilters
from hitsuki.modules.sql import languages_sql as langsql
from hitsuki.modules.rextester.api import Rextester, CompilerError
from hitsuki.modules.rextester.langs import languages
from hitsuki.modules.translations.strings import tld
from hitsuki.modules.helper_funcs.alternate import send_message


SHRUGS = (
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
)
 
HUGS = (
"⊂(・﹏・⊂)",
"⊂(・ヮ・⊂)",
"⊂(・▽・⊂)",
"(っಠ‿ಠ)っ",
"ʕっ•ᴥ•ʔっ",
"（っ・∀・）っ",
"(っ⇀⑃↼)っ",
"(つ´∀｀)つ",
"(.づσ▿σ)づ.",
"⊂(´・ω・｀⊂)",
"(づ￣ ³￣)づ",
"(.づ◡﹏◡)づ.",
)

normiefont = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
weebyfont = ['卂','乃','匚','刀','乇','下','厶','卄','工','丁','长','乚','从','𠘨','口','尸','㔿','尺','丂','丅','凵','リ','山','乂','丫','乙']


@run_async
def shrug(bot: Bot, update: Update):
    # reply to correct message 
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text = reply_text(random.choice(SHRUGS))
 
 
@run_async
def hug(bot: Bot, update: Update):
    # reply to correct message 
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text = reply_text(random.choice(HUGS))


@run_async
def insults(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    text = random.choice(tld(chat.id, "INSULTS-K"))
    update.effective_message.reply_text(text)


@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(random.choice(tld(chat.id, "RUNS-K")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username == "HitaloSama":
            reply_text("Nah, Not doing that")
            return
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld(chat.id, "SLAP_TEMPLATES-K"))
    item = random.choice(tld(chat.id, "ITEMS-K"))
    hit = random.choice(tld(chat.id, "HIT-K"))
    throw = random.choice(tld(chat.id, "THROW-K"))
    itemp = random.choice(tld(chat.id, "ITEMP-K"))
    itemr = random.choice(tld(chat.id, "ITEMR-K"))

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw, itemp=itemp, itemr=itemr)
    # user1=user1, user2=user2, item=item_ru, hits=hit_ru, throws=throw_ru, itemp=itemp_ru, itemr=itemr_ru

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@run_async
def get_bot_ip(bot: Bot, update: Update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@run_async
def get_id(bot: Bot, update: Update, args: List[str]):
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat  # type: Optional[Chat]
    if user_id:
        if update.effective_message.reply_to_message and update.effective_message.reply_to_message.forward_from:
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from
            update.effective_message.reply_text(tld(chat.id,
                                                    "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.").format(
                escape_markdown(user2.first_name),
                user2.id,
                escape_markdown(user1.first_name),
                user1.id),
                parse_mode=ParseMode.MARKDOWN)
        else:
            user = bot.get_chat(user_id)
            update.effective_message.reply_text(
                tld(chat.id, "{}'s id is `{}`.").format(escape_markdown(user.first_name), user.id),
                parse_mode=ParseMode.MARKDOWN)
    else:
        chat = update.effective_chat  # type: Optional[Chat]
        if chat.type == "private":
            update.effective_message.reply_text(tld(chat.id, "Your id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)

        else:
            update.effective_message.reply_text(tld(chat.id, "This group's id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)


@run_async
def info(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat  # type: Optional[Chat]

    if user_id:
        user = bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text(tld(chat.id, "I can't extract a user from this."))
        return

    else:
        return

    text = tld(chat.id, "<b>User info</b>:")
    text += "\nID: <code>{}</code>".format(user.id)
    text += tld(chat.id, "\nFirst Name: {}").format(html.escape(user.first_name))

    if user.last_name:
        text += tld(chat.id, "\nLast Name: {}").format(html.escape(user.last_name))

    if user.username:
        text += tld(chat.id, "\nUsername: @{}").format(html.escape(user.username))

    text += tld(chat.id, "\nUser link: {}").format(mention_html(user.id, "link"))

    if user.id == OWNER_ID:
        text += tld(chat.id, "\n\nThis person is my owner - I would never do anything against them!")
    else:
        if user.id == int(918317361):
            text += tld(chat.id, "\n\nThis person.... He is my god.")

        if user.id in SUDO_USERS:
            text += tld(chat.id, "\n\nThis person is one of my sudo users! " \
                                 "Nearly as powerful as my owner - so watch it.")
        else:
            if user.id in SUPPORT_USERS:
                text += tld(chat.id, "\n\nThis person is one of my support users! " \
                                     "Not quite a sudo user, but can still gban you off the map.")

            if user.id in WHITELIST_USERS:
                text += tld(chat.id, "\n\nThis person has been whitelisted! " \
                                     "That means I'm not allowed to ban/kick them.")

    for mod in USER_INFO:
        mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@run_async
def echo(bot: Bot, update: Update):
    message = update.effective_message
    message.delete()
    args = update.effective_message.text.split(None, 1)
    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)


@run_async
def reply_keyboard_remove(bot: Bot, update: Update):
    reply_keyboard = []
    reply_keyboard.append([
        ReplyKeyboardRemove(
            remove_keyboard=True
        )
    ])
    reply_markup = ReplyKeyboardRemove(
        remove_keyboard=True
    )
    old_message = bot.send_message(
        chat_id=update.message.chat_id,
        text='trying',
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )
    bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=old_message.message_id
    )


@run_async
def markdown_help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(tld(chat.id, "MARKDOWN_HELP-K"), parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(tld(chat.id, "Try forwarding the following message to me, and you'll see!"))
    update.effective_message.reply_text(tld(chat.id, "/save test This is a markdown test. _italics_, *bold*, `code`, "
                                                     "[URL](example.com) [button](buttonurl:github.com) "
                                                     "[button2](buttonurl://google.com:same)"))


@run_async
def stats(bot: Bot, update: Update):
    update.effective_message.reply_text("Current stats:\n" + "\n".join([mod.__stats__() for mod in STATS]))


@run_async
def ping(bot: Bot, update: Update):
    tg_api = ping3('api.telegram.org', count=4)
    google = ping3('google.com', count=4)
    print(google)
    text = "*Pong!*\n"
    text += "Average speed to Telegram bot API server - `{}` ms\n".format(tg_api.rtt_avg_ms)
    if google.rtt_avg:
        gspeed = google.rtt_avg
    else:
        gspeed = google.rtt_avg
    text += "Average speed to Google - `{}` ms".format(gspeed)
    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


LYRICSINFO = "\n[Full Lyrics](http://lyrics.wikia.com/wiki/%s:%s)"


@run_async
def lyrics(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    text = message.text[len('/lyrics '):]
    song = " ".join(args).split("- ")
    reply_text = f'Looks up for lyrics'

    if len(song) == 2:
        while song[1].startswith(" "):
            song[1] = song[1][1:]
        while song[0].startswith(" "):
            song[0] = song[0][1:]
        while song[1].endswith(" "):
            song[1] = song[1][:-1]
        while song[0].endswith(" "):
            song[0] = song[0][:-1]
        try:
            lyrics = "\n".join(PyLyrics.getLyrics(
                song[0], song[1]).split("\n")[:20])
        except ValueError as e:
            return update.effective_message.reply_text("Song %s not found :(" % song[1], failed=True)
        else:
            lyricstext = LYRICSINFO % (song[0].replace(
                " ", "_"), song[1].replace(" ", "_"))
            return update.effective_message.reply_text(lyrics + lyricstext, parse_mode="MARKDOWN")
    else:
        return update.effective_message.reply_text(
            "Invalid syntax! Try Artist - Song name .For example, Luis Fonsi - Despacito", failed=True)


BASE_URL = 'https://del.dog'


@run_async
def paste(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?!")
        return

    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text('Failed to reach dogbin')
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def get_paste_content(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/raw/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    update.effective_message.reply_text('```' + escape_markdown(r.text) + '```', parse_mode=ParseMode.MARKDOWN)


@run_async
def get_paste_stats(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/documents/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    document = r.json()['document']
    key = document['_id']
    views = document['viewCount']
    reply = f'Stats for **[/{key}]({BASE_URL}/{key})**:\nViews: `{views}`'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


@run_async
def ud(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text[len('/ud '):]
    results = get(f'http://api.urbandictionary.com/v0/define?term={text}').json()
    reply_text = f'Word: {text}\nDefinition: {results["list"][0]["definition"]}'
    message.reply_text(reply_text)


@run_async
def execute(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    text = ' '.join(args)
    regex = re.search('^([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$', text, re.IGNORECASE)

    if not regex:
        available_languages = ', '.join(languages.keys())
        message.reply_text('*The availale languages are:*\n`{}`'.format(available_languages),
                           parse_mode=ParseMode.MARKDOWN)
        return

    language = regex.group(1)
    code = regex.group(2)
    stdin = regex.group(3)

    try:
        regexter = Rextester(language, code, stdin)
    except CompilerError as exc:  # Exception on empy code or missing output
        message.reply_text(exc)
        return

    output = ""
    output += "*Language:*\n`{}`".format(language)
    output += "*\n\nSource:*\n`{}`".format(code)

    if regexter.result:
        output += "*\n\nResult:*\n`{}`".format(regexter.result)

    if regexter.warnings:
        output += "\n\n*Warnings:*\n`{}`\n".format(regexter.warnings)

    if regexter.errors:
        output += "\n\n*Errors:*\n'{}`".format(regexter.errors)

    message.reply_text(output, parse_mode=ParseMode.MARKDOWN)


@run_async
def wiki(bot: Bot, update: Update):
	chat = update.effective_chat
	msg = update.effective_message
	chat_id = update.effective_chat.id
	args = update.effective_message.text.split(None, 1)
	teks = args[1]
	message = update.effective_message
	getlang = langsql.get_lang(chat_id)
	if str(getlang) == "en":
		wikipedia.set_lang("en")
	else:
		wikipedia.set_lang("id")
	else:
		wikipedia.set_lang("pt")
	try:
		pagewiki = wikipedia.page(teks)
	except wikipedia.exceptions.PageError:
		send_message(update.effective_message, (tld(chat.id, "No results found")))
		return
	except wikipedia.exceptions.DisambiguationError as refer:
		rujuk = str(refer).split("\n")
		if len(rujuk) >= 6:
			batas = 6
		else:
			batas = len(rujuk)
		teks = ""
		for x in range(batas):
			if x == 0:
				if getlang == "en":
					teks += rujuk[x].replace('pode se referir a', 'may refer to')+"\n"
				else:
					teks += rujuk[x]+"\n"
			else:
				teks += "- `"+rujuk[x]+"`\n"
		send_message(update.effective_message, teks, parse_mode="markdown")
		return
	except IndexError:
		send_message(update.effective_message, (tld(chat.id, "Write a message to search from wikipedia sources")))
		return
	judul = pagewiki.title
	summary = pagewiki.summary
	if update.effective_message.chat.type == "private":
		send_message(update.effective_message, (tld(chat.id, "The result of {} are:\n\n<b>{}</b>\n{}").format(teks, judul, summary)), parse_mode=ParseMode.HTML)
	else:
		if len(summary) >= 200:
			judul = pagewiki.title
			summary = summary[:200]+"..."
			button = InlineKeyboardMarkup([[InlineKeyboardButton(text=(tld(chat.id, "Read more...")), url="t.me/{}?start=wiki-{}".format(bot.username, teks.replace(' ', '_')))]])
		else:
			button = None
		send_message(update.effective_message, (tld(chat.id, "The result of {} are:\n\n<b>{}</b>\n{}").format(teks, judul, summary)), parse_mode=ParseMode.HTML, reply_markup=button)


@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")


def decide(bot: Bot, update: Update):
    chat = update.effective_chat
    r = randint(1, 100)
    if r <= 65:
        update.message.reply_text(tld(chat.id, "Yes."))
    elif r <= 90:
        update.message.reply_text(tld(chat.id, "No."))
    else:
        update.message.reply_text(tld(chat.id, "Maybe."))


@run_async
def gdpr(bot: Bot, update: Update):
    update.effective_message.reply_text("Deleting identifiable data...")
    for mod in GDPR:
        mod.__gdpr__(update.effective_user.id)

    update.effective_message.reply_text("Your personal data has been deleted.\n\nNote that this will not unban "
                                        "you from any chats, as that is telegram data, not Marie data. "
                                        "Flooding, warns, and gbans are also preserved, as of "
                                        "[this](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/), "
                                        "which clearly states that the right to erasure does not apply "
                                        "\"for the performance of a task carried out in the public interest\", as is "
                                        "the case for the aforementioned pieces of data.",
                                        parse_mode=ParseMode.MARKDOWN)


@run_async
def weebify(bot: Bot, update: Update, args):
    msg = update.effective_message
    if args:
        string = " ".join(args).lower()
    elif msg.reply_to_message:
        string = msg.reply_to_message.text.lower()
    else:
        msg.reply_text("Enter some text to weebify or reply to someone's message!")
        return
        
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
 
    if msg.reply_to_message:
        msg.reply_to_message.reply_text(string)
    else:
        msg.reply_text(string)


@run_async
def pat(bot: Bot, update: Update):
    chat_id = update.effective_chat.id
    msg = str(update.message.text)
    try:
        msg = msg.split(" ", 1)[1]
    except IndexError:
        msg = ""
    msg_id = update.effective_message.reply_to_message.message_id if update.effective_message.reply_to_message else update.effective_message.message_id
    pats = []
    pats = json.loads(urllib.request.urlopen(urllib.request.Request(
    'http://headp.at/js/pats.json',
    headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) '
         'Gecko/20071127 Firefox/2.0.0.11'}
    )).read().decode('utf-8'))
    if "@" in msg and len(msg) > 5:
        bot.send_photo(chat_id, f'https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}', caption=msg)
    else:
        bot.send_photo(chat_id, f'https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}', reply_to_message_id=msg_id)


@run_async 
def ping(bot: Bot, update: Update):
    start_time = time.time()
    requests.get('https://api.telegram.org')
    end_time = time.time()
    ping_time = round((end_time - start_time)*1000, 3)
    update.effective_message.reply_text("*Pong!!!*\n`{}ms`".format(ping_time), parse_mode=ParseMode.MARKDOWN)


def shell(command):
    process = Popen(command,stdout=PIPE,shell=True,stderr=PIPE)
    stdout,stderr = process.communicate()
    return (stdout,stderr)


__help__ = """
*Group tools:*
 - /id: get the current group id. If used by replying to a message, gets that user's id.
 - /info: get information about a user.
 - /stickerid: reply to a sticker to me to tell you its file ID.
 - /getsticker: reply to a sticker to me to upload its raw PNG file.
 - /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.

*Useful tools:*
 - /lyrics: Find your favorite songs lyrics!
 - /paste: Create a paste or a shortened url using [dogbin](https://del.dog)
 - /getpaste: Get the content of a paste or shortened url from [dogbin](https://del.dog)
 - /pastestats: Get stats of a paste or shortened url from [dogbin](https://del.dog)
 - /ud: Type the word or expression you want to search. For example /ud Gay
 - /removebotkeyboard: Got a nasty bot keyboard stuck in your group?
 - /exec <language> <code> [/stdin <stdin>]: Execute a code in a specified language. Send an empty command to get the supported languages.
 - /wiki <keywords>: Get wikipedia articles just using this bot!

*Other things:*
 - /runs: reply a random string from an array of replies.
 - /insults: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /decide: Randomly answers yes/no/maybe.
 - /status: Shows some bot information
 - /weebify: as a reply to a message, "weebifies" the message.
 - /pat: give a headpat :3
 - /shg or /shrug: pretty self-explanatory.
 - /hug: give a hug and spread the love :)
"""

__mod_name__ = "Misc"

ID_HANDLER = CommandHandler("id", get_id, pass_args=True, admin_ok=True)
IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID), admin_ok=True)
PING_HANDLER = CommandHandler("ping", ping, admin_ok=True)
LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True, admin_ok=True)

INSULTS_HANDLER = DisableAbleCommandHandler("insults", insults, admin_ok=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True, admin_ok=True)
INFO_HANDLER = CommandHandler("info", info, pass_args=True, admin_ok=True)

ECHO_HANDLER = CommandHandler("echo", echo, filters=Filters.user(OWNER_ID))
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, filters=Filters.private)

STATS_HANDLER = CommandHandler("stats", stats, filters=Filters.user(OWNER_ID))
EXECUTE_HANDLER = CommandHandler("exec", execute, pass_args=True, filters=CustomFilters.sudo_filter)

PASTE_HANDLER = CommandHandler("paste", paste, pass_args=True)
GET_PASTE_HANDLER = CommandHandler("getpaste", get_paste_content, pass_args=True)
PASTE_STATS_HANDLER = CommandHandler("pastestats", get_paste_stats, pass_args=True)
UD_HANDLER = CommandHandler("ud", ud)
WIKI_HANDLER = CommandHandler("wiki", wiki)

DECIDE_HANDLER = CommandHandler("decide", decide)
SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter)

GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.private)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify, pass_args=True)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
SHRUG_HANDLER = DisableAbleCommandHandler(["shrug", "shg"], shrug)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
PING_HANDLER = DisableAbleCommandHandler("ping", ping)

dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(UD_HANDLER)
dispatcher.add_handler(PASTE_HANDLER)
dispatcher.add_handler(GET_PASTE_HANDLER)
dispatcher.add_handler(PASTE_STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(INSULTS_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(LYRICS_HANDLER)
dispatcher.add_handler(DisableAbleCommandHandler("removebotkeyboard", reply_keyboard_remove))
dispatcher.add_handler(EXECUTE_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(GDPR_HANDLER)
dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(PING_HANDLER)
