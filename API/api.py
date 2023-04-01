from aiohttp import ClientSession


class ApiInterface:
    __header: str
    session: ClientSession

    def __init__(self, header: str):
        self.__header = header
        self.session = ClientSession()
