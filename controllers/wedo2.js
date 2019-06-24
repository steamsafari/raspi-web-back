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
     * 启动
     */
    run() {
        var cmd = 'python ' + path.join(path.dirname(__dirname), '/models/py/wedo2.py');
        var wp = child_process.exec(cmd, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Error code: ' + error.code);
                console.log('Signal received: ' + error.signal);
                io.emit('wedo2.run', {
                    code: 1
                });
            } else {
                io.emit('wedo2.run', {
                    code: 0
                });
            }
        });

        return {
            code: 0
        };
    }
}