#!/usr/bin/env python3.7
"""custom recovery downloads scraper"""
# pylint: disable=too-many-locals

from uuid import uuid4

from bs4 import BeautifulSoup
from requests import get
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent, ParseMode

from uranus_bot.modules.mwt import MWT


@MWT(timeout=60 * 60 * 2)
def load_ofrp_data():
    """
    load latest json file every six hours
    :returns data
    """
    return get("https://files.orangefox.tech/Others/update_v2.json").json()


@MWT(timeout=60 * 60 * 2)
def ofrp(device, inline=False):
    """
    fetch latest ofrp links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    data = load_ofrp_data()
    url = f'https://files.orangefox.tech/OrangeFox'
    try:
        info = data[device]
    except KeyError:
        return "", None
    has_beta = False
    name = info['fullname']
    maintainer = info['maintainer']
    message = f'Latest {name} (`{device}`) ' \
              f'[OrangeFox](https://wiki.orangefox.tech/en/home) Builds:\n' \
              f'_Maintainer:_ {maintainer}\n'
    stable = info['stable_build']
    stable_markup = InlineKeyboardButton(f"{stable}", f"{url}-Stable/{device}/{stable}")
    beta_markup = None
    try:
        beta = info['beta_build']
        beta_markup = InlineKeyboardButton(f"{beta}", f"{url}-Beta/{device}/{beta}")
        has_beta = True
    except KeyError:
        pass
    if has_beta:
        keyboard = [[stable_markup], [beta_markup]]
    else:
        keyboard = [[stable_markup]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if inline:
        results = [InlineQueryResultArticle(
            id=uuid4(),
            title=f"Search {device} OrangeFox downloads",
            input_message_content=InputTextMessageContent(
                message, parse_mode=ParseMode.MARKDOWN), reply_markup=reply_markup)]
        return results
    return message, reply_markup
