from abc import ABC, abstractmethod


class StreamHost(ABC):

    def __init__(self, login: str, friendly_name: str = None):
        self.login = login
        self._friendly_name = friendly_name

    def __str__(self):
        return f'{self.__class__.__name__}-{self.login}'

    def __repr__(self):
        return str(StreamHost)

    @property
    def friendly_name(self):
        return self._friendly_name if self._friendly_name else self.login

    @property
    @abstractmethod
    def is_live(self):
        pass

    @abstractmethod
    def get_stream_duration(self):
        pass

    @abstractmethod
    def get_current_viewers(self):
        pass

    @abstractmethod
    def get_credentials(self):
        pass

    @classmethod
    @abstractmethod
    def logo_name(cls):
        pass
