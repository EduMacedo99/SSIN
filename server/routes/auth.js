const express = require('express')
let app = express.Router()

app.get('/', function (req, res) {
    console.log(req.body);
    res.json({"server_public_key": 'sign In'});
});

module.exports = app