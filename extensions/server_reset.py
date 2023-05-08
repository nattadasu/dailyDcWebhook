import requests
from yaml import safe_load
from json import load, dumps
import random
from classes.dataclasses import Character
from typing import Literal, List
from dhooks import Webhook, Embed


with open('config.yaml', 'r') as f:
    config = safe_load(f)

with open('assets/characters.json', 'r') as f:
    characters: dict = load(f)
    charas: list[Character] = []
    for c in characters:
        charas.append(Character(**c))

# random character
chara: Character = random.choice(charas)


def hoyoverse_server_reset_webhook(
    server: Literal[
        'eu',
        'na',
        'sea',
        'tw',
        'global'
    ]
) -> None:
    """Send webhook to Discord server when Hoyoverse's server reset."""
    url: str = config['hoyoverse_server_reset']['webhook']
    hook: Webhook = Webhook(url)
    hook.username = chara.name
    hook.avatar_url = chara.author_icon
    role_list: List[str] = []
    for k, v in config['hoyoverse_server_reset']['roles'][server].items():
        if v:
            role_list.append("<@&" + v + "> ")
    roles: str = ''.join(role_list)
    roles = roles.strip()
    serv: str = ''
    match server:
        case 'eu':
            serv = 'Europe'
        case 'na':
            serv = 'North America'
        case 'sea':
            serv = 'Asia'
        case 'tw':
            serv = 'Mainland China'
        case 'global':
            serv = 'Global/Other'
    games = [
        'Genshin Impact',
        'Tears of Themis',
        'Honkai: Star Rail',
        'Honkai Impact 3rd'
    ]
    if server == 'Global/Other':
        games = [
            'Tears of Themis',
        ]
    elif server == 'Mainland China':
        pass
    else:
        games.remove('Tears of Themis')
    games = '\n'.join(games)
    # data = {
    #     'username': chara.name,
    #     'avatar_url': chara.author_icon,
    #     'content': roles,
    #     'embeds': [
    #         {
    #             'title': 'Hoyoverse\'s Game Server Reset',
    #             'description': 'Hoyoverse\'s server reset is now live!',
    #             'color': chara.color,
    #             'thumbnail': {
    #                 'url': chara.sticker
    #             },
    #             'fields': [
    #                 {
    #                     'name': 'Server',
    #                     'value': server,
    #                     'inline': True
    #                 },
    #                 {
    #                     'name': 'Games',
    #                     'value': games,
    #                     'inline': True
    #                 }
    #             ],
    #             'author': {
    #                 'name': chara.name,
    #                 'url': chara.wiki_uri,
    #                 'icon_url': chara.author_icon
    #             },
    #             'footer': {
    #                 'text': 'Powered by nattadasu/dailyDcWebhook'
    #             }
    #         }
    #     ]
    # }
    embed: Embed = Embed(
        title='Hoyoverse\'s Game Server Reset',
        description='Hoyoverse\' game server reset is done!',
        color=chara.color,
        timestamp='now'
    )

    embed.set_thumbnail(chara.sticker)
    embed.add_field(
        name='Server',
        value=serv,
        inline=True
    )
    embed.add_field(
        name='Games',
        value=games,
        inline=True
    )
    embed.set_author(
        name=chara.name,
        url=chara.wiki_uri,
        icon_url=chara.author_icon
    )
    embed.set_footer(
        text='Powered by nattadasu/dailyDcWebhook'
    )
    hook.send(roles, embed=embed)