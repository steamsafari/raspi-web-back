from gattlib import DiscoveryService
from gattlib import GATTRequester
import os

DELAY = 0.3
InputCommand_hnd = 0x3a
OutputCommand_hnd = 0x3d

RGBAbsoluteMode_cmd = str(
    bytearray(
        [0x01, 0x02, 0x06, 0x17, 0x01, 0x01, 0x00, 0x00, 0x00, 0x02, 0x01]))
RGBAbsoluteOutput_cmd = str(bytearray([0x06, 0x04, 0x03]))


class LED:
    req = None

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

    def run(self):
        # configure RBG LED to Absolute Mode
        self.req.write_by_handle(InputCommand_hnd, RGBAbsoluteMode_cmd)

        # loop all colors
        while True:
            for blue in range(0, 256, 16):
                for green in range(0, 256, 16):
                    for red in range(0, 256, 16):
                        self.req.write_by_handle(
                            OutputCommand_hnd, RGBAbsoluteOutput_cmd +
                            chr(red) + chr(green) + chr(blue))


led = LED()
led.run()
