import time
import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger



# Change uris and sequences according to your setup
URI1 = 'radio://0/70/2M/E7E7E7E701'
URI2 = 'radio://0/70/2M/E7E7E7E702'
URI3 = 'radio://0/70/2M/E7E7E7E703'
URI4 = 'radio://0/70/2M/E7E7E7E704'
URI5 = 'radio://0/70/2M/E7E7E7E705'
URI6 = 'radio://0/70/2M/E7E7E7E706'
URI7 = 'radio://0/70/2M/E7E7E7E707'
URI8 = 'radio://0/70/2M/E7E7E7E708'
URI9 = 'radio://0/70/2M/E7E7E7E709'
URI10 = 'radio://0/100/2M/E7E7E7E7E9'

z0 = 0.4
z = 1.0

x0 = 0.7
x1 = 0
x2 = -0.7

y0 = -1.0
y1 = -0.4
y2 = 0.4
y3 = 1.0

#    x   y   z  time
sequence1 = [
    (x0, y0, z0, 3.0),
    (x0, y0, z, 30.0),
    (x0, y0, z0, 3.0),
]

sequence2 = [
    (x0, y1, z0, 3.0),
    (x0, y1, z, 30.0),
    (x0, y1, z0, 3.0),
]

sequence3 = [
    (x0, y2, z0, 3.0),
    (x0, y2, z, 30.0),
    (x0, y2, z0, 3.0),
]

sequence4 = [
    (x0, y3, z0, 3.0),
    (x0, y3, z, 30.0),
    (x0, y3, z0, 3.0),
]

sequence5 = [
    (x1, y1, z0, 3.0),
    (x1, y1, z, 30.0),
    (x1, y1, z0, 3.0),
]

sequence6 = [
    (x1, y2, z0, 3.0),
    (x1, y2, z, 30.0),
    (x1, y2, z0, 3.0),
]

sequence7 = [
    (x2, y0, z0, 3.0),
    (x2, y0, z, 30.0),
    (x2, y0, z0, 3.0),
]

sequence8 = [
    (x2, y1, z0, 3.0),
    (x2, y1, z, 30.0),
    (x2, y1, z0, 3.0),
]

sequence9 = [
    (x2, y2, z0, 3.0),
    (x2, y2, z, 30.0),
    (x2, y2, z0, 3.0),
]

sequence10 = [
    (x2, y3, z0, 3.0),
    (x2, y3, z, 30.0),
    (x2, y3, z0, 3.0),
]

seq_args = {
    URI1: [sequence1],
    URI2: [sequence2],
    URI3: [sequence3],
    URI4: [sequence4],
    URI5: [sequence5],
    URI6: [sequence6],
    URI7: [sequence7],
    URI8: [sequence8],
    URI9: [sequence9],
    URI10: [sequence10],
}

# List of URIs, comment the one you do not want to fly
uris = {
#    URI1,
#    URI2,
#    URI3,
#    URI4,
#    URI5,
#    URI6,
#    URI7,
#    URI8,
#    URI9,
    URI10
}

def run_sequence(scf, sequence):
    try:
        cf = scf.cf
        cf.param.set_value('flightmode.posSet', '1')

       # take_off(cf, sequence[0])
        for position in sequence:
            print('Setting position {}'.format(position))
            end_time = time.time() + position[3]
            while time.time() < end_time:
       #         cf.commander.send_setpoint(position[1], position[0], 0,
       #                                    int(position[2] * 1000))
                time.sleep(0.1)
       # land(cf, sequence[-1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
	cflib.crtp.init_drivers(enable_debug_driver=False)

	factory = CachedCfFactory(rw_cache='./cache')
	with Swarm(uris, factory=factory) as swarm:
		swarm.parallel(run_sequence, args_dict=seq_args)
