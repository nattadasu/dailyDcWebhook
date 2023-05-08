from dataclasses import dataclass
from typing import Literal

@dataclass
class Character:
    """Character dataclass.

    Attributes:
        name (str): Character's name.
        nick (str): Character's nickname.
        wiki_uri (str): Character's Wikia/DotWiki path.
        origin (Literal['genshin', 'themis', 'hsr', 'honkai']): Character's origin (genshin, themis, hsr, honkai).
        sticker (str): Character's sticker image.
        author_icon (str): Character's author icon.
        color (int): Character's color in decimal.
    """
    name: str
    nick: str
    wiki_uri: str
    origin: Literal['genshin', 'themis', 'hsr', 'honkai']
    sticker: str
    author_icon: str
    color: int
