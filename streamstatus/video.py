import os
import subprocess


class Video:

    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length

    def __str__(self):
        return f'{self.name} ({self.length})'

    def __repr__(self):
        return self.name

    @property
    def length_milliseconds(self):
        return self.length * 1000

    @classmethod
    def get_from_file(cls, path_to_vid):
        name = path_to_vid.split(os.sep)[-1]
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", path_to_vid],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        length = int(float(result.stdout))

        return cls(name, length)


class WelcomeVideo(Video):

    def __init__(self, name: str, length: int):
        super().__init__(name, length)
