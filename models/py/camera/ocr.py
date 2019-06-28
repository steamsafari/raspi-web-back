# coding: utf-8
import picamera
# import numpy as np
from picamera.array import PiRGBAnalysis
import sys
import os
from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
import cv2 as cv
import pytesseract
import re

PORT = int(sys.argv[1])


class MyOcrAnalyzer(PiRGBAnalysis):
    def __init__(self, camera, request_handler):
        super(MyOcrAnalyzer, self).__init__(camera)
        self.request_handler = request_handler
        self.last_ocr_frame = None
        self.last_ocr_digits = ''

    # npimage: numpy array, a rgb frame
    def analyze(self, npimage):
        # 设置一个识别区域
        cv.rectangle(npimage, (110, 80), (210, 160), (0, 255, 0), 2)
        # 获取识别区域rows, columns
        roi_digit = npimage[80:160, 110:210]
        # 将识别区域的图像二值化（黑和白）
        roi_digit_gray = cv.cvtColor(roi_digit, cv.COLOR_BGR2GRAY)
        ret, roi_digit_mono = cv.threshold(roi_digit_gray, 64, 255,
                                           cv.THRESH_BINARY)
        npimage.flags.writeable = True
        for r in range(0, 80):
            for c in range(0, 100):
                npimage[r, c, ] = 0 if roi_digit_mono[r, c] == 0 else 255
        self.request_handler.send_frame(npimage)
        # 检查和上一次做OCR帧的差异，检测到移动再做OCR
        moved = False
        if (self.last_ocr_frame is None):
            moved = True
        else:
            diff = cv.absdiff(self.last_ocr_frame, roi_digit_mono)
            if diff.mean() > 36:  # 超过百分之16的点有变化
                moved = True

        if moved:
            self.last_ocr_frame = roi_digit_mono
            text = pytesseract.image_to_string(roi_digit_mono,
                                               config='--psm 10')
            if len(text.strip()):
                digits = re.sub(r'\D', "", text)
                if (len(digits)):
                    if digits != self.last_ocr_digits:
                        self.last_ocr_digits = digits
                        print(digits, flush=True)


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
                try:
                    camera.start_recording(analyzer, 'rgb')
                    for i in range(1, 61):
                        camera.annotate_text = "frame:{}/60".format(i)
                        camera.wait_recording(1)
                finally:
                    camera.stop_recording()
                    os._exit(0)


def run():
    httpd = HTTPServer(('', PORT), MyRequestHandler)
    print('http server is started', flush=True)
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


# run_in_daemon()

run()
