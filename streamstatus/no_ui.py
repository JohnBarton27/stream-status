import time

from streamstatus.companion import Companion
from streamstatus.light_factory import LightFactory
from streamstatus.spx_gc import SpxGc
from streamstatus.tally_arbiter import TallyArbiter

pi_host = '192.168.2.51'
comp = Companion(pi_host)
tally_arbiter = TallyArbiter(pi_host)
spx = SpxGc(pi_host)
gath_light_factory = LightFactory('192.168.0.104')

apps = [comp, tally_arbiter, spx, gath_light_factory]

while True:
    data = {}
    for application in apps:
        data[application.app_name] = {'status': application.get_is_healthy(), 'time': application.uptime}
        print(f'{application.app_name}: {"UP" if application.get_is_healthy() else "DOWN"} for {application.uptime}')

    print('===========================')
    time.sleep(2)
