var socketio = require('socket.io')(process.env.WS_PORT, {
    path: '/ws'
});
socketio.set('origins', '*:*'); // 解决跨域问题

const redis = require('socket.io-redis');
socketio.adapter(redis({
    host: '127.0.0.1',
    port: 6379,
    key: 'ws'
}));

var mySocketio = {};

mySocketio.getSocketio = function () {
    socketio.on('connection', function (socket) {
        socket.emit('news', {
            hello: 'world'
        });

        socket.on('my other event', function (data) {
            console.log('my other event', data);
        });

        socket.on('disconnect', function () {
            socketio.emit('user disconnected');
        });
    });
}

module.exports = mySocketio;