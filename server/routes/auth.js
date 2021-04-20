const express = require('express')
let app = express.Router()

app.get('/', function (req, res) {
    res.send('SIgn In');
});
app.get('/register', function (req, res) {
    res.send('register' + req.params);
});
module.exports = app