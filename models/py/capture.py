# coding: utf-8
import sys
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
# Camera warm-up time
# sleep(2)

camera.rotation = 180

camera.annotate_text = 'RASPI_WEB'

output = sys.argv[1]

camera.capture(output)
