from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import subprocess
import threading
import time


class PingCheck:

    percent_tolerance = 25
    index = 0
    fig = plt.figure()

    def __init__(self, hostname: str, description: str):
        PingCheck.index += 1
        self.start_time = datetime.now()
        self.hostname = hostname
        self.description = description
        self.average = None
        self.times_called = 0
        self.data_points = []
        self.ax = plt.axes(xlim=(self.start_time.timestamp(), datetime.now().timestamp()), ylim=(0, 150))
        self.line, = self.ax.plot([], [], lw=1)
        print(f"{self.description}: {PingCheck.index}")

    def __str__(self):
        return f'{self.description} ({self.hostname})'

    def __repr__(self):
        return str(self)

    def get_ping(self):
        response = float(subprocess.Popen(["/bin/ping", "-c1", "-w100", self.hostname], stdout=subprocess.PIPE).stdout.read().decode('ascii').split('\n')[1].split('time=')[-1].split(' ')[0])

        if not self.average:
            self.average = response
        else:
            self.average = int((self.average * (self.times_called) + response)/(self.times_called + 1))

        self.times_called += 1

        self.data_points.append((datetime.now(), response))

        return response

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.check_ping()
        x = [val[0].timestamp() for val in self.data_points]
        self.ax.set_xlim(min(x), max(x))
        y = [val[1] for val in self.data_points]
        self.ax.set_ylim(min(y), max(y)*1.5)
        self.line.set_data(x, y)
        return self.line,

    def check_ping(self):
        ping = self.get_ping()

        now = datetime.now().strftime("%H:%M:%S")

        if ping < self.average * (100 - PingCheck.percent_tolerance)/100:
            print(f"{now} Faster than normal - {self} ({ping} vs. {self.average} avg)")

        if ping > self.average * (100 + PingCheck.percent_tolerance)/100:
            print(f"{now} Slower than normal - {self} ({ping} vs. {self.average} avg)")
            return True

        return False

    def ping_listener(self):
        while True:
            time.sleep(1)
            self.check_ping()

    def show_plot(self):
        anim = FuncAnimation(PingCheck.fig, self.animate, init_func=self.init, frames=200, interval=20, blit=True)
        plt.title(self.description)
        plt.show()
