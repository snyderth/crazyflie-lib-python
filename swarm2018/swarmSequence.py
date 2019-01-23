# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017-2018 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Version of the AutonomousSequence.py example connecting to 10 Crazyflies.
The Crazyflies go straight up, hover a while and land but the code is fairly
generic and each Crazyflie has its own sequence of setpoints that it files
to.

The layout of the positions:
    x2      x1      x0

y3  10              4

            ^ Y
            |
y2  9       6       3
            |
            +------> X

y1  8       5       2



y0  7               1

"""
import time

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger

# Change uris and sequences according to your setup
URI1 = 'radio://0/100/2M/E7E7E7E7E0'
URI2 = 'radio://0/100/2M/E7E7E7E7E1'
URI3 = 'radio://0/100/2M/E7E7E7E7E2'
URI4 = 'radio://0/100/2M/E7E7E7E7E3'
URI5 = 'radio://0/100/2M/E7E7E7E7E4'
URI6 = 'radio://0/100/2M/E7E7E7E7E5'
URI7 = 'radio://0/100/2M/E7E7E7E7E6'
URI8 = 'radio://0/100/2M/E7E7E7E7E7'
URI9 = 'radio://0/100/2M/E7E7E7E7E8'
URI10 = 'radio://0/100/2M/E7E7E7E7E9'


z0 = 1.0
z = 1.5

# x0 = 2.8
# x1 = 2.8
# x2 = 3.8
# x3 = 3.8
x0 = 0.5
x1 = 0.5
x2 = 0.5
x3 = 0.5

# y0 = 1.9
# y1 = 2.9
# y2 = 2.9
# y3 = 1.9
y0 = 0.5
y1 = 0.5
y2 = 0.5
y3 = 0.5

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
    (x0, y0, z0, 2.0),
    (x1, y1, z0, 2.0),
    (x2, y2, z0, 2.0),
    (x3, y3, z0, 2.0),
    (x0, y0, z0, 2.0),
]


sequence4 = [
    (0.52,0.59,0.5, 0.5),
    (0.52,0.59,1.0, 10.0),
    (0.52,0.59,0.5, 1.5),
]

# sequence4 = [
#     (x1, y1, z0, 2.0),
#     (x2, y2, z0, 2.0),
#     (x3, y3, z0, 2.0),
#     (x0, y0, z0, 2.0),
#     (x1, y1, z0, 2.0),
# ]

sequence5 = [
    (x1, y0, z0, 3.0),
    (x1, y0, z, 30.0),
    (x1, y0, z0, 3.0),
]

sequence6 = [
    (x2, y2, z0, 2.0),
    (x3, y3, z0, 2.0),
    (x0, y0, z0, 2.0),
    (x1, y1, z0, 2.0),
    (x2, y2, z0, 2.0),
]

sequence7 = [
    (x2, y0, z0, 3.0),
    (x2, y0, z0, 30.0),
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
    (x3, y3, z0, 2.0),
    (x0, y0, z0, 2.0),
    (x1, y1, z0, 2.0),
    (x2, y2, z0, 2.0),
    (x3, y3, z0, 2.0),

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
    # URI1,
    # URI2,
    # URI3,
    #URI4,
    # URI5,
     URI6,
    # URI7,
    # URI8,
    # URI9,
    # URI10
}


def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)

def start_position_printing(scf):
    log_conf = LogConfig(name='Position', period_in_ms=500)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')
    print(scf.cf.link_uri)
    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)


def take_off(cf, position):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = position[2] / take_off_time

    print(vz)

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def land(cf, position):
    landing_time = 1.0
    sleep_time = 0.1
    steps = int(landing_time / sleep_time)
    vz = -position[2] / landing_time

    print(vz)

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)

    cf.commander.send_setpoint(0, 0, 0, 0)
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def run_sequence(scf, sequence):
    try:
        cf = scf.cf
        cf.param.set_value('flightmode.posSet', '1')

        take_off(cf, sequence[0])
        for position in sequence:
            print('Setting position {}'.format(position))
            end_time = time.time() + position[3]
            while time.time() < end_time:
                cf.commander.send_setpoint(position[1], position[0], 0,
                                           int(position[2] * 1000))
                time.sleep(0.1)
        land(cf, sequence[-1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        # swarm.parallel(reset_estimator)

        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)
        swarm.parallel(start_position_printing)
        swarm.parallel(run_sequence, args_dict=seq_args)
