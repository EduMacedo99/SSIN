const express = require('express');
//const sqlite3 = require('sqlite3').verbose();
//const Math = require('Math');
const DBconnect = require('../DBconnect.js');
//const DBtest = require('../databaseTest.js');
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

app.get('/', function (req, res) {
    
    checkSecurityLevel(req, res, () => {
      serviceResponse(req, res);
    });
});

module.exports = app