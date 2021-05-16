const Crypto = require("crypto")
const { TIMEOUT } = require("dns")
const express = require("express")
let app = express.Router()
const net = require("net")
const symmetric = require("../symmetric_encryption")
const db = require("../DBconnect.js")

const CHALLENGE_TIMEOUT = 10

/**
 * Get client data from the BD with username
 */
function getClient(res, username, callback){
  const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
  db.get(sql, (err, row) => {
      if (row == undefined){
        console.log("User not found: " + username)
        res.status(500).json({"msg":"username do not exist on the server."})
      }
      else callback(row)
  })
}

/**
* Encrypt challenge and save challenge encrypted and their expire timeout on the BD
*/
function savaChallenge (username, challenge, timeout, symmetric_key, symmetric_key_iv) {
  // Encrypt challenge
  const enc_challenge =symmetric.encrypt(challenge, symmetric_key_iv, symmetric_key)
  // Update BD
  const sql = "UPDATE users SET challenge=?, challenge_timeout=? WHERE username=?"
  db.run(sql, [enc_challenge, timeout, username], (err, row) => {
      if (err) 
          return console.error(err.message)
      if (row) 
          console.log("Updated BD client: ", row)
  });
}

/**
 * A client sends their username+token, and is asking to start a new session
 * If username+token exists, Authenticator Server sends a challenge (different each time)
 * TODO: put symmetric key + token on the BD in the register phase
 */
app.get("/", function (req, res) {
    const { msg, username, cl_token} = req.body
    console.log("\nStart of authentication ...")
    console.log(" client<  ?  >: " + msg)

    // Check if username and token matches BD
    getClient(res, username, (client) => {
      const { symmetric_key, symmetric_key_iv, token} = client

      const aux_symmetric_key = "wwiimwiegdgcyvdz"
      const aux_symmetric_key_iv = "hsbkjbsmdpgdwfib"
      const aux_token = "this is testing"

      // Decrypt  token
      const token_decrypted = symmetric.decrypt(cl_token, aux_symmetric_key_iv, aux_symmetric_key)
      if(aux_token != token_decrypted){
          res.status(500).json({"msg":"token do not macth this username."})
          return
      }

      // Generate challenge, a unique random value
      const N = Crypto.randomBytes(32).toString("hex")

      // (slides) Protecting against replays needs a nonce or a timestamp
      // (slides) Timestamps need time synchronization which enlarges the attack surface
      // The challenge has a challenge timeout that expires
      const expire_time = Date.now() + CHALLENGE_TIMEOUT

      // Encrypt challenge and save it on the BD, and its expire timeout
      savaChallenge(username, N, expire_time, aux_symmetric_key, aux_symmetric_key_iv)

      res.status(200).json({"msg": username+ "? Prove it, challenge: " + N, challenge: N, timeout: expire_time})
    })
})

/**
 * Client challenge asnwer
 * If client is correct, refresh token
 */
app.get("/challengeRefreshToken", function (req, res) {
  const { msg, username, enc_challenge, port} = req.body
  console.log(" client<" + port + ">: " + msg)

  // Verify if is correct
  // Get symmetric key and encrypted challenge from BD, + timeout
  // TODO: ... 
  const bd_symmetric_key = "wwiimwiegdgcyvdz"
  const bd_iv = "hsbkjbsmdpgdwfib"
  const bd_enc_challenge = ""
  const bd_timeout = 1621181273203555555555
  // Encrypted challenge from BD must be equal to answer
  if(bd_timeout < Date.now()){
    console.log(Date.now())
    res.status(500).json({"msg":"challenge lifetime expired."})
    if(bd_enc_challenge != "")//enc_challenge){
      res.status(500).json({"msg":"Answer do not macth."})
    
    console.log("Authentication failed.")
    return
  }

  // If so, distribute a short-term session key(new token) for being used between the two
  // Create new token
  const new_token = Crypto.randomBytes(12).toString("base64").slice(0, 12)
          
  // Update BD with new token + port of client session
  // TODO: ...

  // Encrypt token
  const enc_token = symmetric.encrypt(new_token, bd_iv, bd_symmetric_key)

  // Send new token to the client
  res.status(200).json({"msg":"okay, it is a match.", token: enc_token})
  console.log("Authentication done.")

})

module.exports = app