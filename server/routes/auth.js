const express = require('express')
let app = express.Router()

app.get('/', function (req, res) {
    res.send('register');
});

module.exports = app