var express = require('express');
var router = express.Router();
var picamera = require('../controllers/picamera');

router.get('/picamera/:action', function (req, res, next) {
    res.json(picamera[req.params.action]());
});

module.exports = router;