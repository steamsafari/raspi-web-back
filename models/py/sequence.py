# coding: utf-8
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import os
import sys

global PORT
PORT = int(sys.argv[1])


# 调用摄像头拍摄图片
class MyCamera:
    bPiCamera = None
    engine = None
    camera = None

    def __init__(self):
        try:
            from picamera import PiCamera
        except ImportError:
            import cv2 as cv

        if 'PiCamera' in dir():
            self.engine = PiCamera
            self.camera = PiCamera()
            self.camera.rotation = 180
            self.camera.resolution = (360, 240)
            self.bPiCamera = True
        else:
            self.engine = cv
            self.camera = cv.VideoCapture(0)
            self.bPiCamera = False

    def capture(self, num):
        if self.bPiCamera:
            frame = BytesIO()
            self.camera.annotate_text = "frame:{}/100".format(num)
            self.camera.capture(frame, 'jpeg')
            return frame.getvalue()
        else:
            ret, frame = self.camera.read()
            _, jpeg = self.engine.imencode('.jpg', frame)
            return jpeg.tobytes()


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 页面输出模板字符串
        self.protocal_version = 'HTTP/1.1'  # 设置协议版本
        self.send_response(200)  # 设置响应状态码
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace;boundary=frame')  # 设置响应头
        self.end_headers()

        camera = MyCamera()
        for num in range(1, 101):
            frameBytes = camera.capture(num)
            self.wfile.write(b'--frame\r\n'
                             b'Content-Type: image/jpeg\r\n\r\n' + frameBytes +
                             b'\r\n')
        os._exit(0)


def run():
    global PORT
    httpd = HTTPServer(('', PORT), MyRequestHandler)
    httpd.serve_forever()


def createDaemon():
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


createDaemon()
