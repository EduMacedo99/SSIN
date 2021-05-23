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
  const { username, cl_token, new_iv, service_id, radicand, index} = req.body

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

    // Decrypt  service_id
    const dec_service_id = symmetric.decrypt(service_id, new_iv, symmetric_key)
    console.log("... client choose service " + dec_service_id + ".")

    // Check security level
    if (parseInt(dec_service_id) <= security_level) {
      console.log("... security level is ok, service level " + dec_service_id + " and client level " + security_level + ".")

      // Dcrypt service data
      const dec_radicand = symmetric.decrypt(radicand, new_iv, symmetric_key)
      let service_data = {"symmetric_key": symmetric_key, "id":dec_service_id, "radicand": dec_radicand}
      if(dec_service_id == 3)
        service_data["index"] = symmetric.decrypt(index, new_iv, symmetric_key)

      callback(service_data)
    }
    else {
      console.log("This user doesnt have permission to this service, service level " + dec_service_id + " and client level " + security_level + ".\n")
      
      // Encrypt msg
      const new_iv_server = symmetric.createNewIV(utils.SIZE)
      const enc_msg = symmetric.encrypt("You don't have permission to this service, service level " + dec_service_id + " and client level " + security_level + ".", new_iv_server, symmetric_key)

      res.status(201).json({"msg": enc_msg, "new_iv":new_iv_server })
    }
  })
}

/**
 * Calculate value
 * TODO: verificar se são mesmo numeros o radicand, index
 */
function serviceResponse (res, service_data) {
  const { id, radicand, index, symmetric_key} = service_data
  var value
  var radicand_float = parseFloat(radicand)
  switch (parseInt(id)) {
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
  
  // Encrypt value msg
  const new_iv_server = symmetric.createNewIV(utils.SIZE)
  const enc_msg = symmetric.encrypt("value = " + value, new_iv_server, symmetric_key)
  
  res.status(200).json({"msg": enc_msg, "new_iv": new_iv_server})
}

/**
 * Check if username and token are valid
 * Update IP address of the client in the DB
 * 
 * TODO: Evitar SQL Injection
 */
app.post('/set_ip', async function (req, res){
  console.log("Set ip ...")
  const {username, ip_address, new_iv} = req.body

  utils.getClient(res, req.body, (client) => {

    // Decrypt ip
    const dec_ip = symmetric.decrypt(ip_address, new_iv, client.symmetric_key)
    console.log("... client " + username + " wants to set a new ip " + dec_ip )

    var sql_set_ip = "UPDATE users SET ip_address=? WHERE username=?"
    DBconnect.run(sql_set_ip, [dec_ip, username], async function (err, row) {
        if (err) {
          res.status(500).json({"msg":err.message})
          return console.error(err.message)
        }
        if (this.changes == 0){
          console.log("No rows to update.\n")

          // Encrypt msg
          const new_iv_server = symmetric.createNewIV(utils.SIZE)
          const enc_msg = symmetric.encrypt("No rows to update", new_iv_server, client.symmetric_key)

          res.status(200).json({"msg": enc_msg, "new_iv": new_iv_server})
        }
        else if (this.changes > 0) {
          console.log(`... Row(s) updated: ${this.changes}`)
          console.log(username + " ip set to " + dec_ip + "\n")

          // Encrypt msg
          const new_iv_server = symmetric.createNewIV(utils.SIZE)
          const enc_msg = symmetric.encrypt(username + " ip set to " + dec_ip, new_iv_server, client.symmetric_key)

          res.status(200).json({"msg": enc_msg, "new_iv": new_iv_server})
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

  const {username, username_2, new_iv} = req.body

  utils.getClient(res, req.body, (client) => {

    // Decrypt username_2
    const dec_username_2 = symmetric.decrypt(username_2, new_iv, client.symmetric_key)
    console.log("... client " + username + " wants to know ip of " + dec_username_2)

    var sql_get_ip = "SELECT ip_address FROM users WHERE username=?"
    DBconnect.get(sql_get_ip, [dec_username_2], (err, row) => {
      if (err) {
        res.status(500).json({"msg":err.message})
        return console.error(err.message)
      }
      if (row == undefined || row.ip_address == null){
        console.log("The " + dec_username_2 + " you want to talk not found.\n")
        res.status(500).json({"msg": "The client you want to talk not found."})
      }
      else if (row.ip_address == "NOT_AVAILABLE"){
        console.log(dec_username_2 + " ip is " + row.ip_address + "\n")
        res.status(501).json({"msg": "The client you want to talk is not available right now."})
      }
      else {
        // Encrypt msg
        const new_iv_server = symmetric.createNewIV(utils.SIZE)
        const enc_msg = symmetric.encrypt(dec_username_2 + " ip is " + row.ip_address, new_iv_server, client.symmetric_key)
        
        console.log(dec_username_2 + " ip is " + row.ip_address + "\n")
        res.status(200).json({"msg": enc_msg, "ip_port": row.ip_address, "new_iv": new_iv_server})
      }
    })
  })

})


app.get('/public_key', function (req, res) {
  console.log("Start service ...")
  const username_2 = req.body.username_2
  var sql_get_ip = "SELECT public_key FROM users WHERE username=?"
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
      console.log(username_2 + " pub key is " + row.public_key + "\n")
      res.status(row.public_key != null ? 200 : 500).json({"public_key": row.public_key})
    }
  })

})


app.get('/', function (req, res) {
  console.log("Start service ...")

    checkSecurityLevel(req, res, (service_data) => {
      serviceResponse(res, service_data)
    })
})

module.exports = app