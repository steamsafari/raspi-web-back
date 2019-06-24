var express = require('express');
var router = express.Router();
var picamera = require('../controllers/picamera');
var wedo2 = require('../controllers/wedo2');

router.get('/picamera/:action', function (req, res) {
    res.json(picamera[req.params.action]());
});

router.get('/wedo2/:action', function (req, res) {
    res.json(wedo2[req.params.action]());
});

module.exports = router;