import time
import logging
import cflib
from cflib.crazyflie import Crazyflie


if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    URI = 'radio://0/100/2M'
    cf = Crazyflie()
    #cf.connected.add_callback()
    cf.open_link(URI)
    thrust_mult = 1
    thrust_step = 500
    thrust = 20000
    pitch = 0
    roll = 0
    yawrate = 0

    # Unlock startup thrust protection
    cf.commander.send_setpoint(0, 0, 0, 0)

    while thrust >= 20000:
        cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
        time.sleep(0.1)
        if thrust >= 25000:
            thrust_mult = -1
        thrust += thrust_step * thrust_mult
    cf.commander.send_setpoint(0, 0, 0, 0)
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)
    cf.close_link()
