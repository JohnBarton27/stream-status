from abc import ABC, abstractmethod


class Application(ABC):

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

    def __str__(self):
        return f'{self.app_name} ({self.hostname}:{self.port})'

    def __repr__(self):
        return str(self)

    @property
    @abstractmethod
    def app_name(self):
        pass

    @property
    def url(self):
        return f'http://{self.hostname}:{self.port}'

    @abstractmethod
    def get_is_healthy(self):
        pass
