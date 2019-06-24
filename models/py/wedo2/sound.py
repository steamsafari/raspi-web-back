from gattlib import DiscoveryService
from gattlib import GATTRequester
from time import sleep
import os

OutputCommand_hnd = 0x3d

Sound_cmd = str(bytearray([0x05, 0x02, 0x04]))

Note_a = str(bytearray([0xB8, 0x01]))
Note_b = str(bytearray([0xD2, 0x01]))
Note_c = str(bytearray([0x05, 0x01]))
Note_f = str(bytearray([0x5D, 0x01]))
Note_aH = str(bytearray([0x70, 0x03]))
Note_cH = str(bytearray([0x0B, 0x02]))
Note_dH = str(bytearray([0x4B, 0x02]))
Note_eH = str(bytearray([0x93, 0x02]))
Note_fH = str(bytearray([0xBA, 0x02]))
Note_gH = str(bytearray([0x10, 0x03]))
Note_gS = str(bytearray([0x9F, 0x01]))
Note_cSH = str(bytearray([0x2A, 0x02]))
Note_dSH = str(bytearray([0x6E, 0x02]))
Note_gSH = str(bytearray([0x3E, 0x03]))
Note_fSH = str(bytearray([0xE4, 0x02]))
Note_aS = str(bytearray([0xC7, 0x01]))


class Sound:
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

    def volume_up():
        pass

    def volume_down():
        pass

    def play(self, note, seconds):
        duration = int(seconds * 1000)
        low = duration & 0x00FF
        high = duration >> 8
        print('low:{},high:{}'.format(hex(low), hex(high)))
        duration_bits = str(bytearray([low, high]))
        cmd = Sound_cmd + note + duration_bits
        self.req.write_by_handle(OutputCommand_hnd, cmd)
        sleep(seconds)


sound = Sound()
sound.play(Note_a, .5)
sound.play(Note_a, .5)
sound.play(Note_a, .5)
sound.play(Note_f, .35)
sound.play(Note_cH, .15)
sound.play(Note_a, .5)
sound.play(Note_f, .35)
sound.play(Note_cH, .15)
sound.play(Note_a, 1)
sound.play(Note_eH, .5)
sound.play(Note_eH, .5)
sound.play(Note_eH, .5)
sound.play(Note_fH, .35)
sound.play(Note_cH, .15)
sound.play(Note_gS, .5)
sound.play(Note_f, .35)
sound.play(Note_cH, .15)
sound.play(Note_a, 1)
sound.play(Note_aH, .5)
sound.play(Note_a, .35)
sound.play(Note_a, .15)
sound.play(Note_aH, .5)
sound.play(Note_gSH, .25)
sound.play(Note_gH, .25)
sound.play(Note_fSH, .125)
sound.play(Note_fH, .125)
sound.play(Note_fSH, .25)
sleep(.25)
sound.play(Note_aS, .25)
sound.play(Note_dSH, .5)
sound.play(Note_dH, .25)
sound.play(Note_cSH, .25)
sound.play(Note_cH, .125)
sound.play(Note_b, .125)
sound.play(Note_cH, .25)
sleep(.25)
sound.play(Note_f, .125)
sound.play(Note_gS, .5)
sound.play(Note_f, .375)
sound.play(Note_a, .125)
sound.play(Note_cH, .5)
sound.play(Note_a, .375)
sound.play(Note_cH, .125)
sound.play(Note_eH, 1)
sound.play(Note_aH, .5)
sound.play(Note_a, .35)
sound.play(Note_a, .15)
sound.play(Note_aH, .5)
sound.play(Note_gSH, .25)
sound.play(Note_gH, .25)
sound.play(Note_fSH, .125)
sound.play(Note_fH, .125)
sound.play(Note_fSH, .25)
sleep(.25)
sound.play(Note_aS, .25)
sound.play(Note_dSH, .5)
sound.play(Note_dH, .25)
sound.play(Note_cSH, .25)
sound.play(Note_cH, .125)
sound.play(Note_b, .125)
sound.play(Note_cH, .25)
sleep(.25)
sound.play(Note_f, .25)
sound.play(Note_gS, .5)
sound.play(Note_f, .375)
sound.play(Note_cH, .125)
sound.play(Note_a, .5)
sound.play(Note_f, .375)
sound.play(Note_c, .125)
sound.play(Note_a, 1)
