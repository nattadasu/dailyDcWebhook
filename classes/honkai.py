import requests
from fake_useragent import FakeUserAgent as UserAgent
from yaml import safe_load as load

from .excepts import HoyoverseException
from modules.commons import define_hoyoverse_retcode

ua = UserAgent(browsers=['chrome', 'edge'])
config: dict = load(open("config.yaml", "r", encoding="utf-8").read())
key = config["keys"]["hoyoverse"]
ltuid = key["ltuid"]
ltoken = key["ltoken"]
webhook = config["hoyoverse_daily_checkin"]["webhook"]


class Honkai:
    def __init__(
        self,
        ltuid: str = ltuid,
        ltoken: str = ltoken,
    ) -> None:
        """Honkai Impact 3rd HoYoLab Daily Check-In

        Args:
            ltuid (str): ltuid. Defaults to ltuid defined in config.keys.hoyoeverse.ltuid.
            ltoken (str): ltoken. Defaults to ltoken defined in config.keys.hoyoeverse.ltoken.

        Raises:
            Exception: Missing HoYoLab auth cookie value.

        Returns:
            None: None.
        """
        self.ltuid: str = ltuid
        self.ltoken: str = ltoken
        if not self.ltuid or not self.ltoken:
            raise ValueError("Missing HoYoLab auth cookie value.")
        self.check_in_uri = "https://sg-public-api.hoyolab.com/event/mani/sign"

    def check_in(self):
        """Check in to Hoyoverse's HoYoLab daily check-in.

        Raises:
            Exception: Known errors.
        """
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,ar;q=0.7,ja;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'ltuid=' + self.ltuid + '; ltoken=' + self.ltoken,
            'DNT': '1',
            'Origin': 'https://act.hoyolab.com',
            'Referer': 'https://act.hoyolab.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua.random,
            'sec-gpc': '1'
        }

        data = {
            'act_id': 'e202110291205111'
        }

        url = f"{self.check_in_uri}" + "?lang=en-us"

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            resp = response.json()
            define_hoyoverse_retcode(resp["retcode"], resp["message"])
        else:
            raise HoyoverseException(
                f"HTTP {response.status_code} {response.reason}")
