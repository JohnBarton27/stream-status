from datetime import datetime


class Event:

    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time

    def __str__(self):
        return f'{self.name} ({self.time})'

    def __repr__(self):
        return str(self)

    @property
    def has_happened(self):
        return datetime.now() > self.time

    def get_time_remaining(self):
        if self.has_happened:
            return -1

        time_delta = self.time - datetime.now()

        hours = time_delta.seconds // 3600
        minutes = (time_delta.seconds // 60) % 60
        seconds = time_delta.seconds - (minutes * 60)

        if minutes < 10:
            minutes = f'0{minutes}'

        if seconds < 10:
            seconds = f'0{seconds}'

        td_str = f'{f"{hours}:" if hours != 0 else ""}{minutes}:{seconds}'

        return td_str
