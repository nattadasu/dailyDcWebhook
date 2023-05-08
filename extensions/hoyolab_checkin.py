import random
import time
from dataclasses import dataclass
from json import load
from typing import Literal

import requests
from yaml import safe_load

from classes.genshin import Genshin
from classes.honkai import Honkai
from classes.starrail import StarRail
from classes.themis import Themis
from modules.commons import now_to_cst
from classes.dataclasses import Character   


def list_today_reward() -> dict[str, str]:
    """List today's rewards for Hoyoverse's HoYoLab daily sign in.

    Returns:
        dict[str, str]: Today's rewards for Genshin Impact, Tears of Themis, Honkai: Star Rail, and Honkai Impact 3rd.
    """
    with open('assets/genshin.json', 'r') as f:
        gi_rewards = load(f)
    with open('assets/themis.json', 'r') as f:
        tot_rewards = load(f)
    with open('assets/starrail.json', 'r') as f:
        hsr_rewards = load(f)
    with open('assets/honkai.json', 'r') as f:
        hi3_rewards = load(f)

    now: str = now_to_cst().strftime('%d')
    rewards = {
        'gi': gi_rewards[now],
        'tot': tot_rewards[now],
        'hsr': hsr_rewards[now],
        'hi3': hi3_rewards[now]
    }

    return rewards


def get_random_character() -> Character:
    """Get a random character from assets/characters.json array.

    Returns:
        Character: Character's name, images, Wikia path, and color in decimal.
    """
    with open('assets/characters.json', 'r') as f:
        characters = load(f)

    chara: dict = random.choice(characters)
    wiki: str = chara['wiki_uri']
    wiki_uri: str = ''
    match chara['origin']:
        case 'genshin':
            wiki_uri = f'https://genshin-impact.fandom.com/wiki/{wiki}'
        case 'themis':
            wiki_uri = f'https://tot.wiki/wiki/{wiki}'
        case 'hsr':
            wiki_uri = f'https://honkai-star-rail.fandom.com/wiki/{wiki}'
        case 'honkai':
            wiki_uri = f'https://honkaiimpact3.fandom.com/wiki/{wiki}'
    return Character(
        name=chara['name'],
        nick=chara['nick'],
        wiki_uri=wiki_uri,
        origin=chara['origin'],
        sticker=chara['sticker'],
        author_icon=chara['author_icon'],
        color=chara['color']
    )

def get_banner(origin: Literal['genshin', 'themis', 'hsr', 'honkai']) -> str:
    """Get a banner from specified game name

    Returns:
        str: Banner's url
    """
    banners = {
        'genshin': 'https://static.wikia.nocookie.net/gensin-impact/images/8/81/HoYoLAB_Community_Daily_Check-In.png/revision/latest?cb=20210301043650',
        'themis': 'https://media.discordapp.net/attachments/1078005713349115964/1078023098202325043/XyOd4HYLzM7QOopC.png',
        'hsr': 'https://static.wikia.nocookie.net/houkai-star-rail/images/7/7e/Event_Honkai_Star_Rail_Daily_Check-in.png',
        'honkai': 'https://static.wikia.nocookie.net/honkaiimpact3_gamepedia_en/images/1/19/HoYoLAB_Daily_Sign-in_%28Banner%29.png'
    }
    return banners[origin]

def webhook_mihoyo_event_sign(
    is_genshin: bool = False,
    is_themis: bool = False,
    is_starrail: bool = False,
    is_honkai: bool = False,
) -> None:
    """Send an embed to Discord's webhook for Hoyoverse's HoYoLab daily sign in.

    Args:
        is_genshin (bool): Was the author checked in to Genshin Impact? Defaults to False.
        is_themis (bool): Was the author checked in to Tears of Themis? Defaults to False.
        is_starrail (bool): Was the author checked in to Honkai: Star Rail? Defaults to False.
        is_honkai (bool): Was the author checked in to Honkai Impact 3rd? Defaults to False.

    Returns:
        None
    """

    rewards = list_today_reward()
    chara = get_random_character()

    gi = '✅' if is_genshin else '❌'
    tot = '✅' if is_themis else '❌'
    hsr = '✅' if is_starrail else '❌'
    hi3 = '✅' if is_honkai else '❌'

    banner = get_banner(chara.origin)

    hyl: dict = {
        'gi': 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481&lang=en-us',
        'tot': 'https://act.hoyolab.com/bbs/event/signin/nxx/index.html?act_id=e202202281857121&lang=en-us',
        'hsr': 'https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html?act_id=e202303301540311&lang=en-us',
        'hi3': 'https://act.hoyolab.com/bbs/event/signin-bh3/index.html?act_id=e202110291205111&lang=en-us'
    }

    embeds = [{
        'title': 'Heya! It\'s time to claim your daily reward!',
        'fields': [
            {
                'name': 'Today\'s Rewards',
                'value': f'**Genshin Impact:** {rewards["gi"]}\n**Tears of Themis:** {rewards["tot"]}\n**Honkai: Star Rail:** {rewards["hsr"]}\n**Honkai Impact 3rd:** {rewards["hi3"]}',
                'inline': False
            },
            {
                'name': 'Auto Check In Status',
                'value': f'**Genshin Impact:** {gi}\n**Tears of Themis:** {tot}\n**Honkai: Star Rail:** {hsr}\n**Honkai Impact 3rd:** {hi3}',
                'inline': True
            },
            {
                'name': 'Check In Links',
                'value': f'[**Genshin Impact**]({hyl["gi"]})\n[**Tears of Themis**]({hyl["tot"]})\n[**Honkai: Star Rail**]({hyl["hsr"]})\n[**Honkai Impact 3rd**]({hyl["hi3"]})',
                'inline': True
            }
        ],
        'color': chara.color,
        'author': {
            'name': chara.nick,
            'url': chara.wiki_uri,
            'icon_url': chara.author_icon
        },
        'thumbnail': {
            'url': chara.sticker
        },
        'image': {
            'url': banner
        },
        'footer': {
            'text': 'Powered by nattadasu/dailyDcWebhook'
        }
    }]

    with open('config.yaml', 'r') as f:
        config = safe_load(f)

    roles = ""

    for k, v in config['hoyoverse_daily_checkin']['roles'].items():
        if v in ['', None]:
            continue
        roles += f'<@&{v}> '

    roles = roles.strip()

    discord_webhook = {
        'content': roles,
        'embeds': embeds,
        'avatar_url': chara.author_icon,
        'username': chara.name
    }

    if config['hoyoverse_daily_checkin']['webhook']['_global'] in [None, '']:
        for k, v in config['hoyoverse_daily_checkin']['webhook'].items():
            if k == '_global':
                continue
            if v in ['', None]:
                continue
            webhook = requests.post(v, json=discord_webhook)
            print(f'Webhook {k} status: {webhook.status_code}')
            time.sleep(0.5)
    else:
        webhook = requests.post(config['hoyoverse_daily_checkin']['webhook']['_global'], json=discord_webhook)
        print(f'Webhook status: {webhook.status_code}')


def hoyoverse_daily_checkin():
    gi = False
    tot = False
    hsr = False
    hi3 = False

    try:
        Genshin().check_in()
        gi = True
    except Exception as e:
        print(f'GI: {e}')

    try:
        Themis().check_in()
        tot = True
    except Exception as e:
        print(f'ToT: {e}')

    try:
        StarRail().check_in()
        hsr = True
    except Exception as e:
        print(f'HSR: {e}')

    try:
        Honkai().check_in()
        hi3 = True
    except Exception as e:
        print(f'HI3: {e}')

    webhook_mihoyo_event_sign(
        is_genshin=gi,
        is_themis=tot,
        is_starrail=hsr,
        is_honkai=hi3
    )