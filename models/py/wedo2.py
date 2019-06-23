from gattlib import DiscoveryService
from gattlib import GATTRequester
from time import sleep

HANDLE = 0x3d
SPIN_LEFT = str(bytearray([0x01, 0x01, 0x01, 0x64]))
SPIN_RIGHT = "\x01\x01\x01\x9C"
SPIN_STOP = "\x01\x01\x01\x00"
DELAY = 30
WEDO_DELAY = 0.3
BUTTON_WIDTH = 45
MAX_SPEED = 100
MIN_SPEED = 1
SPEED_CHANGE = 4

current_speed = 100
req = None


def motor_up():
    global req, current_speed
    if req is not None:
        if current_speed == MAX_SPEED:
            return

        current_speed += SPEED_CHANGE
        req.write_by_handle(HANDLE,
                            str(bytearray([0x01, 0x01, 0x01, current_speed])))
        sleep(WEDO_DELAY)


def motor_down():
    global req, current_speed
    if req is not None:
        if current_speed == MIN_SPEED:
            return

        current_speed -= SPEED_CHANGE
        req.write_by_handle(HANDLE,
                            str(bytearray([0x01, 0x01, 0x01, current_speed])))
        sleep(WEDO_DELAY)


def motor_run():
    global req
    if req is not None:
        req.write_by_handle(HANDLE, SPIN_LEFT)


def motor_stop():
    global req
    if req is not None:
        req.write_by_handle(HANDLE, SPIN_STOP)


def smart_hub_disconnect():
    global req
    if req is not None:
        req.disconnect()


def smart_hub_connect():
    service = DiscoveryService("hci0")
    devices = service.discover(2)

    for address, name in devices.items():
        if name != '' and 'nemo-wedo2' in name:
            print(name)
            global req
            req = GATTRequester(address, True, "hci0")
            break


smart_hub_connect()

if req is not None:
    motor_run()
    sleep(20)
