const Crypto = require("crypto")
const { TIMEOUT } = require("dns")
const express = require("express")
let app = express.Router()
const net = require("net")
const symmetric = require("../symmetric_encryption")

const CHALLENGE_TIMEOUT = 10

/**
 * A client sends their username+token, and is asking to start a new session
 * If username+token exists, Authenticator Server sends a challenge (different each time)
 */
app.get("/", function (req, res) {
    const { msg, username, token} = req.body
    console.log("\nStart of authentication ...")
    console.log(" client<  ?  >: " + msg)

    // If username exists on the BD, get symmetric key
    // TODO: ... 
    const bd_symmetric_key = "wwiimwiegdgcyvdz"
    const bd_iv = "hsbkjbsmdpgdwfib"
    const bd_token = "this is testing"
    // Decrypt  token
    const token_decrypted = symmetric.decrypt(token, bd_iv, bd_symmetric_key)
    // Check if token is the same on the BD
    if(bd_token != token_decrypted){
      res.status(500).json({"msg":"username or token doesnt match."})
      return
    }

    // Generate challenge, a unique random value
    const N = Crypto.randomBytes(32).toString("hex")

    // (slides) Protecting against replays needs a nonce or a timestamp
    // (slides) Timestamps need time synchronization which enlarges the attack surface
    // The challenge has a challenge timeout that expires
    const expire_time = Date.now() + CHALLENGE_TIMEOUT

    // Encrypt challenge and save it on the BD, and its expire timeout
    const enc_challenge = symmetric.encrypt(N,  bd_iv, bd_symmetric_key)
    // TODO: ...

    res.status(200).json({"msg": username+ "? Prove it, challenge: " + N, challenge: N, timeout: expire_time})

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
      res.status(500).json({"msg":"Answer does not macth."})
    
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