from datetime import datetime, timedelta


class Event:

    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time
        self.id = name.replace(' ', '-').lower()

    def __str__(self):
        return f'{self.name} ({self.time})'

    def __repr__(self):
        return str(self)

    @property
    def has_happened(self):
        return datetime.now() > self.time

    @property
    def _seconds_remaining(self):
        return (self.time - datetime.now()).seconds

    @property
    def in_danger_zone(self):
        return self._seconds_remaining < 60

    @property
    def in_extreme_danger_zone(self):
        return self._seconds_remaining < 10

    def get_time_remaining(self):
        if self.has_happened:
            return -1

        time_delta = self._seconds_remaining

        hours = time_delta // 3600
        minutes = (time_delta // 60) % 60
        seconds = time_delta - (minutes * 60)

        if minutes < 10:
            minutes = f'0{minutes}'

        if seconds < 10:
            seconds = f'0{seconds}'

        td_str = f'{f"{hours}:" if hours != 0 else ""}{minutes}:{seconds}'

        return td_str


class SundayEvent(Event):

    def __init__(self, name: str, hour: int, minute: int = 0, second: int = 0):
        sunday = SundayEvent.get_next_sunday()
        time = datetime(year=sunday.year, month=sunday.month, day=sunday.day, hour=hour, minute=minute, second=second)
        super().__init__(name, time)

    @staticmethod
    def get_next_sunday():
        sunday = datetime.now()

        while sunday.weekday() != 6:
            sunday = sunday + timedelta(days=1)

        return sunday
