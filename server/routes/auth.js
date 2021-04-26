const express = require('express')
let app = express.Router()

app.get('/', function (req, res) {
    console.log(req.body);
});

module.exports = app