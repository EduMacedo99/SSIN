const express = require('express')
const DBconnect = require('../DBconnect.js').db
let app = express.Router()
const symmetric = require("../symmetric_encryption")
const utils = require("../utils")

/**
 * Check if username and token are valid
 * Check if client has permission to this service by checking their security level
 * If they have, call callback
 * 
 * TODO: Evitar SQL Injection
 */
function checkSecurityLevel(req, res, callback) {
  const { username, cl_token, new_iv, service_data} = req.body

  console.log("... checking if username and token macthes DB.")

  var sql = `SELECT * FROM users WHERE username = "`+ username +'"'
  DBconnect.get(sql, (err, row) => {
    if (row == undefined){
      console.log("User not found: " + username)
      res.status(500).json({"msg":"User not found: " + username})
      return
    }
    const { symmetric_key, token, security_level} = row

    // Decrypt  token
    const token_decrypted = symmetric.decrypt(cl_token, new_iv, symmetric_key)
    if(token != token_decrypted){
      console.log("Authentication failed - token do not macth this username.")
      res.status(500).json({"msg":"Token do not macth this username."})
      return
    }
    console.log("... valid username and token.")

    // Check security level
    if (parseInt(service_data.service_id) <= security_level) {
      console.log("... security level is ok, service level " + service_data.service_id + " and client level " + security_level + ".")
      callback()
    }
    else {
      console.log("This user doesnt have permission to this service, service level " + service_data.service_id + " and client level " + security_level + ".\n")
      res.status(500).json({"msg":"You don't have permission to this service, service level " + service_data.service_id + " and client level " + security_level + "."})
    }
  })
}

/**
 * Calculate value
 * TODO: verificar se são mesmo numeros o radicand, index
 */
function serviceResponse (req, res) {
  const { service_id, radicand, index } = req.body.service_data
  var value
  var radicand_float = parseFloat(radicand)
  switch (parseInt(service_id)) {
    case 1:
      value = Math.sqrt(radicand_float)
      break
    case 2:
      value = Math.pow(radicand_float, 1 / 3)
      break
    case 3:
      value = Math.pow(radicand_float, 1 / parseFloat(index))
      break
  }
  console.log("Service done. Value = " + value + "\n")
  res.status(200).json({"msg":"value = " + value})
}

/**
 * Check if username and token are valid
 * Update IP address of the client in the DB
 * 
 * TODO: Evitar SQL Injection
 */
app.post('/set_ip', async function (req, res){
  console.log("Set ip ...")

  const {username, ip_address} = req.body

  utils.getClient(res, req.body, () => {
    var sql_set_ip = "UPDATE users SET ip_address=? WHERE username=?"
    DBconnect.run(sql_set_ip, [ip_address], async function (err, row) {
        if (err) {
          res.status(500).json({"msg":err.message})
          return console.error(err.message)
        }
        if (this.changes == 0){
          console.log("No rows to update.")
          res.status(200).json({"msg":"No rows to update"})
        }
        else if (this.changes > 0) {
          console.log(`... Row(s) updated: ${this.changes}`)
          console.log(username + " ip set to " + ip_address + "\n")
          res.status(201).json({"msg": username + " ip set to " + ip_address})
        }
      })
    })

  })

/**
 * Check if username and token are valid
 * Return ip or "USER_NOT_FOUND"
 * 
 * TODO: Evitar SQL Injection
 */
app.get('/get_ip', function(req, res){
  console.log("Get ip ...")

  const {username_2, ip_address} = req.body

  utils.getClient(res, req.body, () => {
    var sql_get_ip = "SELECT ip_address FROM users WHERE username=?"
    DBconnect.get(sql_get_ip, [username_2], (err, row) => {
      if (err) {
        res.status(500).json({"msg":err.message})
        return console.error(err.message)
      }
      if (row == undefined){
        console.log(username_2 + " that you want to talk not found.\n")
        res.status(500).json({"msg": username_2 + " that you want to talk not found."})
      }
      else {
        console.log(username_2 + " ip is " + row.ip_address + "\n")
        res.status(201).json({"msg": username_2 + " ip is " + row.ip_address, "ip_port": row.ip_address})
      }
    })
  })

})

app.get('/', function (req, res) {
  console.log("Start service ...")

    checkSecurityLevel(req, res, () => {
      serviceResponse(req, res)
    })
})

module.exports = app