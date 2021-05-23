const sqlite3 = require('sqlite3');
const DBconnect = require('./DBconnect.js').db
const symmetric = require("./symmetric_encryption")

/**
* Save token and symmetric key in DB
*
* TODO: Evitar SQL Injection
*/
function saveClientRegistration (username, token, symmetric_key) {
  const sql = "UPDATE users SET token=?, symmetric_key=? WHERE username=?"
  DBconnect.run(sql, [token, symmetric_key, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  });
}

/**
* Save challenge and their expire timeout on the DB
*
* TODO: Evitar SQL Injection
*/
function saveChallenge (username, challenge, timeout) {
  const sql = "UPDATE users SET challenge=?, challenge_timeout=? WHERE username=?"
  DBconnect.run(sql, [challenge, timeout, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  })
}

/**
* Save new token and ip_port of client session
*
* TODO: Evitar SQL Injection
*/
function saveClientNewSession (username, token, ip_port) {
    const sql = "UPDATE users SET token=?, ip_address=? WHERE username=?"
    DBconnect.run(sql, [token, ip_port, username], async function (err, row) {
      if (err) {
        return console.error(err.message);
      }
    })
}

/**
 * Get client data from the DB with username
 */
function getClient(res, username, callback){
    const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
    DBconnect.get(sql, (err, row) => {
        if (row == undefined){
          console.log("Authentication failed - User not found.")
          res.status(500).json({"msg":"User not found."})
        }
        else callback(row)
    })
}

/**
 * Get client data from the DB with username if token is correct
 */
 function getClient(res, config, callback){
    const { username, cl_token, new_iv} = config

    const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
    DBconnect.get(sql, (err, row) => {
        if (row == undefined){
          console.log("User not found.")
          res.status(500).json({"msg":"User not found."})
        }
        else{ 
            console.log("... checking if username and token macthes DB.")
            // Check if username and token matches DB
            const { symmetric_key, token} = row
            // Decrypt  token
            const token_decrypted = symmetric.decrypt(cl_token, new_iv, symmetric_key)
            
            if(token != token_decrypted){
                console.log("Token do not macth this username.")
                res.status(500).json({"msg":"Token do not macth this username."})
                return
            }
            console.log("... valid username and token.")
            callback(row)
        }
    })
}


module.exports = {
    saveClientRegistration,
    saveChallenge,
    saveClientNewSession,
    getClient
}