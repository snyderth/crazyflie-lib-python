import cflib.crtp
from cflib.drivers.crazyradio import Crazyradio
URI1='0xE7E7E7E7E0'
URI2='0xE7E7E7E7E1'
URI3='0xE7E7E7E7E2'
URI4=0xE7E7E7E7E3
URI5=0xE7E7E7E7E4
URI6=0xE7E7E7E7E5
URI7=0xE7E7E7E7E6
URI8='0xE7E7E7E7E7'
URI9=0xE7E7E7E7E8
URI10=0xE7E7E7E7E9
cflib.crtp.init_drivers(enable_debug_driver=False)



cr = Crazyradio()

cr.set_channel(100)
cr.set_data_rate(cr.DR_2MPS)
# cr.set_address(hex(0xE7E7E7E7E7))

cr.send_packet((0xff, 0xfe, 0xff)).ack   # Init the reboot
# print cr.send_packet((0xff, 0xfe, 0xf0, 0)).ack   # Reboot to Bootloader
while not cr.send_packet((0xff, 0xfe, 0xf0, 1)).ack: # Reboot to Firmware
    #keep trying
    print("trying again") 
