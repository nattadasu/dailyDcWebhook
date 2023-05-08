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


class Themis:
    def __init__(
        self,
        ltuid: str = ltuid,
        ltoken: str = ltoken,
    ) -> None:
        """Tears of Themis HoYoLab Daily Check-In

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
        self.check_in_uri = "https://sg-public-api.hoyolab.com/event/luna/os/sign"

    def check_in(self):
        """Check in to Hoyoverse's HoYoLab daily check-in.

        Raises:
            Exception: Known errors.
        """
        headers = {
            "User-Agent": ua.random,
            "Referer": "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202202281857121&lang=en-us",
        }
        data = {
            "act_id": "e202202281857121",
            "lang": "en-us",
        }
        cookies = {
            "ltuid": self.ltuid,
            "ltoken": self.ltoken
        }
        response = requests.post(
            self.check_in_uri, headers=headers, params=data, cookies=cookies)
        resp = response.json()
        if response.status_code == 200:
            resp = response.json()
            define_hoyoverse_retcode(resp["retcode"], resp["message"])
        else:
            raise HoyoverseException(
                f"HTTP {response.status_code} {response.reason}")
