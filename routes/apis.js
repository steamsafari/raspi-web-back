var express = require('express');
var router = express.Router();
var camera = require('../controllers/camera');
var wedo2 = require('../controllers/wedo2');

router.get('/camera/:action', function (req, res) {
    res.json(camera[req.params.action]());
});

router.get('/wedo2/:action', function (req, res) {
    res.json(wedo2[req.params.action]());
});

module.exports = router;