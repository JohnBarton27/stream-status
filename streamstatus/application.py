from abc import ABC, abstractmethod
from datetime import datetime


class Application(ABC):

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        self._first_healthy = None
        self._first_unhealthy = None

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

    @property
    @abstractmethod
    def is_up(self):
        pass

    @property
    def uptime(self):
        uptime = None
        if self._first_healthy:
            uptime = datetime.now() - self._first_healthy
        elif self._first_unhealthy:
            uptime = datetime.now() - self._first_unhealthy
        if uptime.seconds < 60:
            return f'{uptime.seconds} sec'
        else:
            return f'{uptime.seconds//60} min'

    def get_is_healthy(self):
        if self.is_up:
            if not self._first_healthy:
                self._first_healthy = datetime.now()
                self._first_unhealthy = None
            return True

        else:
            if not self._first_unhealthy:
                self._first_unhealthy = datetime.now()
                self._first_healthy = None
            return False
