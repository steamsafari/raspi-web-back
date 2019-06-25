/**
 * picamera模块apis
 */
var path = require('path');
const child_process = require('child_process');
var io = require('socket.io-emitter')({
    host: '127.0.0.1',
    port: 6379,
    key: 'ws'
});

module.exports = {
    /**
     * 拍摄1张图片
     */
    capture() {
        var fs = require('fs');

        // 递归创建目录 同步方法
        function mkdirsSync(dirname) {
            if (fs.existsSync(dirname)) {
                return true;
            } else {
                if (mkdirsSync(path.dirname(dirname))) {
                    fs.mkdirSync(dirname);
                    return true;
                }
            }
        }

        var relativeOutputDir = '/storage/picamera/capture/';
        var absoluteOutputDir = process.cwd() + relativeOutputDir;
        mkdirsSync(absoluteOutputDir);

        var filename = 'foo.jpg';
        var cmd = 'python3 ' + path.join(path.dirname(__dirname), '/models/py/picamera/capture.py') + ' ' + absoluteOutputDir + filename;
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('picamera.capture', {
                    code: 1
                });
            } else {
                //console.log('stdout: ' + stdout);
                console.log('stream server started');
                io.emit('picamera.capture', {
                    code: 0,
                    file: relativeOutputDir + filename
                });
            }
        });

        return {
            code: 0
        };
    },
    /**
     * 拍摄图片流
     */
    sequence() {
        var cmd = 'python3 ' + path.join(path.dirname(__dirname), '/models/py/picamera/sequence.py') + ' 3002';
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('picamera.sequence', {
                    code: 1
                });
            } else {
                console.log('stream server started');
                var ip = require('ip');
                io.emit('picamera.sequence', {
                    code: 0,
                    file: 'http://' + ip.address() + ':3002/'
                });
            }
        });

        return {
            code: 0
        };
    },
    /**
     * 检测颜色
     */
    detectColor() {
        var cmd = 'python3 ' + path.join(path.dirname(__dirname), '/models/py/picamera/detect_color.py') + ' 3002';
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('picamera.detectColor', {
                    code: 1
                });
            } else {
                console.log('stream server started');
                var ip = require('ip');
                io.emit('picamera.detectColor', {
                    code: 0,
                    file: 'http://' + ip.address() + ':3002/'
                });
            }
        });

        return {
            code: 0
        };
    },
    /**
     * 检测手势
     */
    detectGesture() {
        const spawn = child_process.spawn;
        const wp = spawn('python3', [path.join(path.dirname(__dirname), '/models/py/picamera/detect_gesture.py')])

        wp.stdout.on('data', function (stdout) {
            let gestures = stdout.toString().replace('\n', '');
            gestures = gestures.split(' ');
            io.emit('picamera.detectGesture', {
                code: 0,
                data: gestures
            });
        });
        wp.on('close', function () {
            io.emit('picamera.detectGesture', {
                code: 0,
                data: 'exit'
            });
        });

        return {
            code: 0
        };
    }
}