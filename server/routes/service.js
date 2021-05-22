const express = require('express');
const DBconnect = require('../DBconnect.js').db;
let app = express.Router()

function checkSecurityLevel(req, res, callback) {
  
  var username = req.query.username;
  var sql = `SELECT *
          FROM users
          WHERE username = "`+ username +'"';
  DBconnect.get(sql, (err, row) => {
    if (row == undefined){
      console.log("User not found: " + username);
      res.send("User not found: " + username);
      return;
    }

    var securityLevel = row.security_level;
    if (parseInt(req.query.service) <= securityLevel) {
      console.log("security level is ok");
      callback();
    }
    else {
      console.log("This user doesnt have permission to this service");
      res.send("You don't have permission to this service");
    }
  });
}

function serviceResponse (req, res) {
  var value;
  var service = parseInt(req.query.service);
  var radicand = parseFloat(req.query.radicand);
  var index = parseFloat(req.query.index);
  switch (service) {
    case 1:
      value = Math.sqrt(radicand);
      break;
    case 2:
      value = Math.pow(radicand, 1 / 3);
      break;
    case 3:
      value = Math.pow(radicand, 1 / index);
      break;
  }
  res.send("value = " + value);
}






app.post('/set_ip', async function (req, res){
  var sql_set_ip = "UPDATE users SET ip_address=?";
  DBconnect.run(sql_set_ip, [req.query.ip_address], async function (err, row) {
      if (err) {
        return console.error(err.message);
      }
      if (this.changes == 0){
        console.log(`User ${req.query.username} not found`);
        console.log("No rows to update");
        res.sendStatus(500)
      }
      else if (this.changes > 0) {
        console.log(`Row(s) updated: ${this.changes}`);
        console.log(req.query.username + " ip set to " + req.query.ip_address);
        res.sendStatus(201)
      }
    });
  });

app.post('/get_ip', function(req, res){
  
  var sql_get_ip = "SELECT ip_address FROM users WHERE username=?";
  DBconnect.get(sql_get_ip, [req.query.username], (err, row) => {
    if (err) {
      return console.error(err.message);
    }
    if (row == undefined){
      res.send("USER_NOT_FOUND");
    }
    else {
      res.send("ip = "+row.ip_address);
    }
  });
});



app.get('/', function (req, res) {
    checkSecurityLevel(req, res, () => {
      serviceResponse(req, res);
    });
});

module.exports = app