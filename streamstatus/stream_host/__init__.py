from abc import ABC, abstractmethod


class StreamHost(ABC):

    def __init__(self, login):
        self.login = login

    def __str__(self):
        return f'{self.__class__.__name__}-{self.login}'

    def __repr__(self):
        return str(StreamHost)

    @property
    @abstractmethod
    def is_live(self):
        pass

    @abstractmethod
    def get_current_viewers(self):
        pass

    @abstractmethod
    def get_credentials(self):
        pass
