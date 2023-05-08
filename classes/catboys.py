#!/usr/bin/env python3

import requests
import json
from yaml import safe_load as load
from datetime import datetime


class CatBoys:
    def __init__(self):
        config = load(open("config.yaml", "r", encoding="utf-8").read())
        self.webhook = config["daily_images"]["webhooks"]["nekomimi_boy"]
        self.headers = {
            "Content-Type": "application/json"
        }
        self.catboys_url = "https://api.catboys.com/img"
        self.catboys_default_attribution = "Artwork by unknown artist.\nKnow the artist? [Contact team](https://catboys.com/contact) (image URI: <{}>)"
        self.embed = {
            "title": "Your daily cat boys image is here!",
            "color": 0x673AB7,
            "author": {
                "name": "CatBoys",
                "icon_url": "https://catboys.com/favicon.png"
            },
            "footer": {
                "text": "Powered by Natsu's Laptop (acting as server) and Python"
            },
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }

    def invoke_catboys(self):
        catboys = requests.get(self.catboys_url).json()

        if catboys['artist'] != 'unknown':
            attribution = f"Artwork by [{catboys['artist']}]({catboys['artist_url']}). [Sauce]({catboys['source_url']})"
        else:
            attribution = self.catboys_default_attribution.format(
                catboys['url'])

        # Update embed with image URL and attribution
        self.embed.update({
            "description": attribution,
            "image": {"url": catboys['url']}
        })

        # Send webhook
        discord_message = {
            "content": "",
            "username": "CatBoys",
            "avatar_url": "https://catboys.com/favicon.png",
            "embeds": [self.embed]
        }

        requests.post(self.webhook, data=json.dumps(
            discord_message), headers=self.headers)
