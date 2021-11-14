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
    def _days_remaining(self):
        return (self.time - datetime.now()).days

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
        seconds = time_delta - (minutes * 60) - (hours * 3600)

        if minutes < 10:
            minutes = f'0{minutes}'

        if seconds < 10:
            seconds = f'0{seconds}'

        days_str = ''
        if self._days_remaining > 0:
            days_str = f'{self._days_remaining} day'
            days_str = f'{days_str}s ' if self._days_remaining > 1 else f'{days_str} '

        hrs_str = f'{hours}:' if hours != 0 else ''

        td_str = f'{days_str}{hrs_str}{minutes}:{seconds}'

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


class Service(SundayEvent):

    def __init__(self, name: str, hour: int, minute: int = 0, advance_stream_start_min: int = 5, welcome=None):
        super().__init__(name, hour, minute)
        self.advance_stream_start_min = advance_stream_start_min
        self.welcome = welcome

    def get_all_events(self):
        stream_start = Event(f'{self.name} Stream Start', self.time - timedelta(minutes=self.advance_stream_start_min))
        if self.welcome:
            welcome_video_start = Event(f'{self.name} Welcome Video Start', self.time - timedelta(seconds=self.welcome.length))
            return [stream_start, welcome_video_start, self]

        return [stream_start,  self]
