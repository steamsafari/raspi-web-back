# coding: utf-8
import picamera
import numpy as np
from picamera.array import PiRGBAnalysis
from picamera.color import Color
import sys
import os
from io import BytesIO
from PIL import Image
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(sys.argv[1])


class MyColorAnalyzer(PiRGBAnalysis):
    def __init__(self, camera, request_handler):
        super(MyColorAnalyzer, self).__init__(camera)
        self.last_detected_color = ''
        self.request_handler = request_handler

    # a: numpy array, a rgb frame
    def analyze(self, a):
        # Convert the average color of the pixels in the middle box
        color = Color(r=int(np.mean(a[30:60, 60:120, 0])),
                      g=int(np.mean(a[30:60, 60:120, 1])),
                      b=int(np.mean(a[30:60, 60:120, 2])))
        # Convert the color to hue, saturation, lightness
        h, l, s = color.hls
        detected = 'none'
        if s > 1 / 3:
            if h > 8 / 9 or h < 1 / 36:
                detected = 'red'
            elif 5 / 9 < h < 2 / 3:
                detected = 'blue'
            elif 5 / 36 < h < 4 / 9:
                detected = 'green'

        # If the color has changed, update the display
        if detected != self.last_detected_color:
            print('detect color:{}'.format(detected))
            self.last_detected_color = detected
            # convert numpy array to jpeg
            im = Image.fromarray(a)
            imagebytes = BytesIO()
            im.save(imagebytes, format='JPEG')
            imagedata = imagebytes.getvalue()

            self.request_handler.send_frame(imagedata)


class MyRequestHandler(BaseHTTPRequestHandler):
    def send_frame(self, frameBytes):
        self.wfile.write(b'--frame\r\n')
        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', len(frameBytes))
        self.end_headers()
        self.wfile.write(frameBytes)
        self.wfile.write(b'\r\n')

    def do_GET(self):
        # 页面输出模板字符串
        self.protocal_version = 'HTTP/1.1'  # 设置协议版本
        self.send_response(200)  # 设置响应状态码
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace;boundary=frame')  # 设置响应头
        self.end_headers()

        with picamera.PiCamera(resolution='320x180', framerate=24) as camera:
            # camera.rotation = 180
            with MyColorAnalyzer(camera, self) as analyzer:
                camera.start_recording(analyzer, 'rgb')
                camera.wait_recording(60)
                camera.stop_recording()
                os._exit(0)


def run():
    httpd = HTTPServer(('', PORT), MyRequestHandler)
    print('http server is started')
    httpd.serve_forever()


def run_in_daemon():
    # fork进程
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError as error:
        print('fork #1 failed: %d (%s)', error.errno, error.strerror)
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print('Daemon PID %d', pid)
            os._exit(0)
    except OSError as error:
        print('fork #2 failed: %d (%s)', error.errno, error.strerror)
        os._exit(1)
    # 重定向标准IO
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    run()


run_in_daemon()
