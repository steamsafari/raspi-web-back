# coding: utf-8
import picamera
# import numpy as np
from picamera.array import PiRGBAnalysis
import sys
import os
from io import BytesIO
from PIL import Image
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(sys.argv[1])


class MyOcrAnalyzer(PiRGBAnalysis):
    def __init__(self, camera, request_handler):
        super(MyOcrAnalyzer, self).__init__(camera)
        self.request_handler = request_handler

    # npimage: numpy array, a rgb frame
    def analyze(self, npimage):
        self.request_handler.send_frame(npimage)


class MyRequestHandler(BaseHTTPRequestHandler):
    def send_frame(self, npimage):
        # convert numpy array to jpeg
        im = Image.fromarray(npimage)
        imagebytes = BytesIO()
        im.save(imagebytes, format='JPEG')
        imagedata = imagebytes.getvalue()
        # send image
        self.wfile.write(b'--frame\r\n')
        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', len(imagedata))
        self.end_headers()
        self.wfile.write(imagedata)
        self.wfile.write(b'\r\n')

    def do_GET(self):
        # 页面输出模板字符串
        self.protocal_version = 'HTTP/1.1'  # 设置协议版本
        self.send_response(200)  # 设置响应状态码
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace;boundary=frame')  # 设置响应头
        self.end_headers()

        with picamera.PiCamera(resolution='320x240', framerate=24) as camera:
            camera.rotation = 180
            with MyOcrAnalyzer(camera, self) as analyzer:
                camera.start_recording(analyzer, 'rgb')
                camera.wait_recording(30)
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
