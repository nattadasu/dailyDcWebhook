import requests
import json
from yaml import safe_load as load
import random
import re
from datetime import datetime
from fake_useragent import UserAgent

ua = UserAgent(browsers=['edge', 'firefox', 'chrome'])


class ZeroChan:
    def __init__(self, is_girl: bool = True):
        config = load(open("config.yaml", "r", encoding="utf-8").read())
        uastr = ua.random
        whook = config["daily_images"]["webhooks"]
        self.webhook = whook["nekomimi_girl"] if is_girl else whook["nekomimi_boy"]
        self.headers = { "Content-Type": "application/json", "User-Agent": uastr }
        tags = ["Nekomimi", "Solo", "Female" if is_girl else "Male"]
        tags_str = ",".join(tags)
        self.zerochan_url = f"https://www.zerochan.net/{tags_str}?json"
        self.zerochan_default_source = "None"
        self.img = "Furina.full.4040497.png" if is_girl else r"Chat.Noir.%28Ladybug%29.full.4025125.jpg"
        self.embed = {
            "title": f"Your daily cat {'girl' if is_girl else 'boy'} image is here!",
            "color": 0x87387F,
            "author": {
                "name": "ZeroChan",
                "icon_url": f"https://static.zerochan.net/{self.img}"
            },
            "footer": {"text": "Powered by github:nattadasu/dailyDcWebhook"},
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "fields": [
                {"name": "Image Source", "value": self.zerochan_default_source, "inline": True},
                {"name": "Source Title/Artist", "value": "", "inline": True},
                {"name": "ID", "value": "", "inline": True}
            ]
        }

    def invoke_img(self):
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
        id_val = f"[`{random_id}`](https://zerochan.net/{random_id})"

        # Update the embed with the image information
        self.embed.update({
            "description": f"**Tags**\n{tags}",
            "image": {"url": img_url},
            "fields": [
                {"name": "Image Source","value": source,"inline": True},
                {"name": "Source Title/Artist", "value": meta_data["primary"], "inline": True},
                {"name": "ID", "value": id_val, "inline": True }
            ]
        })

        # Send the webhook
        discord_message = { "content": "", 
                            "username": "ZeroChan",
                            "avatar_url": f"https://static.zerochan.net/{self.img}",
                            "embeds": [self.embed] }

        requests.post(self.webhook, data=json.dumps(discord_message), headers={"Content-Type": "application/json"})
