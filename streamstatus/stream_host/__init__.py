from abc import ABC, abstractmethod


class StreamHost(ABC):

    def __init__(self):
        pass

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
