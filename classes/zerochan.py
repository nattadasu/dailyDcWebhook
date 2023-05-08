import requests
import json
from yaml import safe_load as load
import random
import re
from datetime import datetime
from fake_useragent import UserAgent

ua = UserAgent(browsers=['edge', 'firefox', 'chrome'])


class ZeroChan:
    def __init__(self):
        config = load(open("config.yaml", "r", encoding="utf-8").read())
        uastr = ua.random
        self.webhook = config["daily_images"]["webhooks"]["nekomimi_girl"]
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": uastr
        }
        self.zerochan_url = "https://www.zerochan.net/Nekomimi,Female?json"
        self.zerochan_default_source = "None"
        self.embed = {
            "title": "Your daily cat girl image is here!",
            "color": 0x87387F,
            "author": {
                "name": "ZeroChan",
                "icon_url": "https://static.zerochan.net/Nahida.full.3803289.jpg"
            },
            "footer": {
                "text": "Powered by github:nattadasu/dailyDcWebhook"
            },
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "fields": [
                {
                    "name": "Image Source",
                    "value": self.zerochan_default_source,
                    "inline": True
                },
                {
                    "name": "Source Title/Artist",
                    "value": "",
                    "inline": True
                },
                {
                    "name": "ID",
                    "value": "",
                    "inline": True
                }
            ]
        }

    def invoke_catgirls(self):
        # Get image metadata from ZeroChan API
        zerochan_data = requests.get(
            self.zerochan_url, headers=self.headers).text

        # Extract IDs from the metadata using regex
        ids_regex = '"id":\s*(\d+),'
        ids_matches = re.findall(ids_regex, zerochan_data)

        # Convert the IDs to integers and select a random ID
        random_id = int(random.choice(ids_matches))

        # Get metadata for the selected ID
        meta_url = f"https://www.zerochan.net/{random_id}?json"
        meta_data: dict = requests.get(meta_url, headers=self.headers).json()

        # Get image URL and tags from metadata
        img_url = meta_data["full"]
        tags = ", ".join(sorted(meta_data["tags"]))

        # Get image source information
        source = meta_data.get("source", None) or self.zerochan_default_source

        # Update the embed with the image information
        self.embed.update({
            "description": f"**Tags**\n{tags}",
            "image": {"url": img_url},
            "fields": [
                {
                    "name": "Image Source",
                    "value": source,
                    "inline": True
                },
                {
                    "name": "Source Title/Artist",
                    "value": meta_data["primary"],
                    "inline": True
                },
                {
                    "name": "ID",
                    "value": f"[`{random_id}`](https://zerochan.net/{random_id})",
                    "inline": True
                }
            ]
        })

        # Send the webhook
        discord_message = {
            "content": "",
            "username": "ZeroChan",
            "avatar_url": "https://static.zerochan.net/Nahida.full.3803289.jpg",
            "embeds": [self.embed]
        }

        requests.post(self.webhook, data=json.dumps(discord_message), headers={
            "Content-Type": "application/json"
        })
