from gattlib import DiscoveryService
from gattlib import GATTRequester
from time import sleep
import os

HANDLE = 0x3d
SPIN_LEFT = str(bytearray([0x01, 0x01, 0x01, 0x64]))
SPIN_RIGHT = "\x01\x01\x01\x9C"
SPIN_STOP = "\x01\x01\x01\x00"
DELAY = 30
WEDO_DELAY = 0.3
MAX_SPEED = 100
MIN_SPEED = 1
SPEED_CHANGE = 4


class Motor:
    req = None
    current_speed = 100

    def __init__(self):
        service = DiscoveryService("hci0")
        devices = service.discover(2)

        for address, name in devices.items():
            if name != '' and 'nemo-wedo2' in name:
                print(name)
                req = GATTRequester(address, True, "hci0")
                break

        if 'req' not in dir():
            print('Connecting to wedo2.0 hub is failed!')
            os._exit(0)

        self.req = req

    def left(self, seconds):
        if self.req is not None:
            self.req.write_by_handle(HANDLE, SPIN_LEFT)
            sleep(seconds)

    def right(self, seconds):
        if self.req is not None:
            self.req.write_by_handle(HANDLE, SPIN_RIGHT)
            sleep(seconds)

    def down(self):
        if self.req is not None:
            if self.current_speed == MIN_SPEED:
                return

            self.current_speed -= SPEED_CHANGE
            self.req.write_by_handle(
                HANDLE, str(bytearray([0x01, 0x01, 0x01, self.current_speed])))
            sleep(WEDO_DELAY)

    def up(self):
        if self.req is not None:
            if self.current_speed == MAX_SPEED:
                return

            self.current_speed += SPEED_CHANGE
            self.req.write_by_handle(
                HANDLE, str(bytearray([0x01, 0x01, 0x01, self.current_speed])))
            sleep(WEDO_DELAY)

    def stop(self):
        if self.req is not None:
            self.req.write_by_handle(HANDLE, SPIN_STOP)

    def smart_hub_disconnect(self):
        if self.req is not None:
            self.req.disconnect()


motor = Motor()
motor.left(1)
for s in range(1, 16):
    motor.down()
motor.right(1)
for s in range(1, 16):
    motor.up()
