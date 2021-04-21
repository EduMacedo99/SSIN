const express = require('express')
let app = express.Router()

app.get('/', function (req, res) {
    res.send('choose a sevice');
});

module.exports = app