class HoyoverseException(Exception):
    """Hoyoverse Exceptions"""

    def __init__(self, retcode: int | str, message: str) -> None:
        """Hoyoverse Exceptions

        Args:
            retcode (int | str): retcode.
            message (str): message.
        """
        if isinstance(retcode, int):
            retcode = str(retcode)
        self.retcode = retcode
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"HoyoverseException: {self.retcode} - {self.message}"


__all__ = [
    "HoyoverseException"
]
