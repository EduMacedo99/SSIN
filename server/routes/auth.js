const Crypto = require("crypto")
const express = require("express")
let app = express.Router()
const net = require("net")
const symmetric = require("../symmetric_encryption")
const DB = require("../DBconnect.js")
const utils = require("../utils")

const CHALLENGE_TIMEOUT = 10

/**
 * Get client data from the DB with username
 */
 function getClient(res, username, callback){
  const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
  DB.db.get(sql, (err, row) => {
      if (row == undefined){
        console.log("Authentication failed - User not found.")
        res.status(500).json({"msg":"User not found."})
      }
      else callback(row)
  })
}


/**
 * A client sends their username+token, and is asking to start a new session
 * If username+token exists, Authenticator Server sends a challenge (different each time)
 */
app.get("/", function (req, res) {
    const { msg, username } = req.body
    console.log("Start of authentication ...")
    console.log("... client< ? >: " + msg)

    utils.getClient(res, req.body, (client) => {

      // Generate challenge, a unique random value
      const N = Crypto.randomBytes(32).toString("hex")

      // (slides) Protecting against replays needs a nonce or a timestamp
      // (slides) Timestamps need time synchronization which enlarges the attack surface
      // The challenge has a challenge timeout that expires
      const expire_time = Date.now() + CHALLENGE_TIMEOUT

      // Save challenge on the DB, and its expire timeout
      utils.saveChallenge(username, N, expire_time, client.symmetric_key)

      res.status(200).json({"msg": username+ "? Prove it, challenge: " + N, challenge: N, timeout: expire_time})
    })
})

/**
 * Client challenge asnwer
 * If client is correct, refresh token
 */
app.get("/challengeRefreshToken", function (req, res) {
  const { msg, username, enc_challenge, ip_port, new_iv} = req.body
  console.log("... client<" + ip_port + ">: " + msg)

  // Verify if is correct
  // Get symmetric key and encrypted challenge from DB, + timeout
  getClient(res, username, (client) => {
    const { challenge, timeout, symmetric_key } = client

    // Check challenge lifetime
    if(timeout < Date.now()){
      console.log("Authentication failed - challenge lifetime expired.")
      res.status(500).json({"msg":"Challenge lifetime expired."})
      return
    }
    // Decrypt challenge answer
    const dec_challenge = symmetric.decrypt(enc_challenge, new_iv, symmetric_key)
    // Encrypted challenge from DB must be equal to answer: enc_challenge
    if(challenge != dec_challenge){
      console.log("Authentication failed - answer do not macth.")
      res.status(500).json({"msg":"Answer do not macth."})
      return
    }

    // (slides) If so, distribute a short-term session key(new token) for being used between the two
    // Create new token
    const new_token = Crypto.randomBytes(12).toString("base64").slice(0, 12)
            
    // Update DB with new token + ip_port of client session
    utils.saveClientNewSession (username, new_token, ip_port)

    // Encrypt new token
    const enc_token = symmetric.encrypt(new_token, new_iv, symmetric_key)

    // Send new token to the client
    res.status(200).json({"msg":"Okay, it is a match.", token: enc_token})
    console.log("Authentication done.\n")
  })
})

module.exports = app