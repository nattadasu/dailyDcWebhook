from datetime import datetime, timedelta, timezone
from classes.excepts import HoyoverseException


def now_to_cst() -> datetime:
    """Returns current datetime in CST.

    Returns:
        datetime: Current datetime in CST.
    """
    now = datetime.now(timezone.utc)
    return now.astimezone(timezone(timedelta(hours=8)))


def define_hoyoverse_retcode(retcode: str | int, message: str) -> HoyoverseException:
    """Defines Hoyoverse return codes (retcode) and raises HoyoverseException.

    Args:
        retcode (str | int): retcode.
        message (str): message.

    Raises:
        HoyoverseException: HoyoverseException.
    """
    if isinstance(retcode, int):
        retcode = str(retcode)
    match retcode:
        case "0":
            print("Successfully checked in.")
        case "-100":
            raise HoyoverseException(
                retcode, "Token expired, not logged in, or invalid token.")
        case "-502":
            raise HoyoverseException(retcode, "Something went wrong.")
        case "-5003":
            raise HoyoverseException(retcode, "Already checked in.")
        case "-10001":
            raise HoyoverseException(retcode, "Invalid request.")
        case "-10002":
            raise HoyoverseException(retcode, "Account can't be found.")
        case "-500015":
            raise HoyoverseException(
                retcode, "Configuration error. Submit an issue on GitHub.")
        case _:
            raise HoyoverseException(retcode, message)
