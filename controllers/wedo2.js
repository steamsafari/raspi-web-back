/**
 * wedo2.0模块apis
 */
var path = require('path');
var child_process = require('child_process');
var io = require('socket.io-emitter')({
    host: '127.0.0.1',
    port: 6379,
    key: 'ws'
});

module.exports = {
    /**
     * 马达
     */
    motor() {
        var cmd = 'python ' + path.join(path.dirname(__dirname), '/models/py/wedo2/motor.py');
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('wedo2.motor', {
                    code: 1
                });
            } else {
                io.emit('wedo2.motor', {
                    code: 0
                });
            }
        });

        return {
            code: 0
        };
    },
    /**
     * LED灯
     */
    led() {
        var cmd = 'python ' + path.join(path.dirname(__dirname), '/models/py/wedo2/led.py');
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('wedo2.led', {
                    code: 1
                });
            } else {
                io.emit('wedo2.led', {
                    code: 0
                });
            }
        });

        return {
            code: 0
        };
    }
}