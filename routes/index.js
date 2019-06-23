var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
  res.sendFile('main.html', {
    root: './public'
  });
});

/* GET picamera page. */
router.get('/picamera', function (req, res, next) {
  res.sendFile('picamera.html', {
    root: './public'
  });
});

/* GET wedo2 page. */
router.get('/wedo2', function (req, res, next) {
  res.sendFile('wedo2.html', {
    root: './public'
  });
});

module.exports = router;