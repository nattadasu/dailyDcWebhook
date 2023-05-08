import requests
import json
from yaml import safe_load as load
from datetime import datetime


class TheCatApi:
    def __init__(self):
        config = load(open("config.yaml", "r", encoding="utf-8").read())
        try:
            self.webhook = config["daily_images"]["webhooks"]["cats"]
        except KeyError:
            raise KeyError(
                "TheCatApi webhook not found in config.yaml. Please add it.")
        try:
            self.apikeys = config["keys"]["thecatapi"]
        except KeyError:
            raise KeyError(
                "TheCatApi API key not found in config.yaml. Please add it.")
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.apikeys["apikey"]
        }
        self.thecatsapi_url = "https://api.thecatapi.com/v1/images/"


    def invoke_cats(self):
        response = requests.get(
            f"{self.thecatsapi_url}search",
            headers=self.headers
        ).json()

        image_id = response[0]["id"]

        response = requests.get(
            f"{self.thecatsapi_url}{image_id}",
            headers=self.headers
        ).json()

        breeds = []
        for breed in response.get("breeds", []):
            breeds.append({
                "name": breed["name"],
                "value": f"""**Origin**: {breed['origin']}
**Weight**: {breed['weight']['metric']} kg
**Life Span**: {breed['life_span']} years
**Temperament**: {breed['temperament']}""",
                "inline": True
            })

        self.embed = {
            "title": "Your daily cat image is here!",
            "color": 0x000000,
            "author": {
                "name": "TheCatApi",
                "icon_url": "https://thecatapi.com/favicon.ico",
                "url": "https://thecatapi.com/"
            },
            "footer": {
                "text": "Powered by github:nattadasu/dailyDcWebhook in Python",
            },
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "image": {
                "url": response["url"],
            },
            "fields": breeds
        }

        discord_message = {
            "content": "",
            "username": "TheCatApi",
            "avatar_url": "https://i0.wp.com/thatapicompany.com/wp-content/uploads/2021/07/logo-trsp.png",
            "embeds": [self.embed]
        }

        requests.post(
            self.webhook,
            json=discord_message,
            headers={"Content-Type": "application/json"}
        )

