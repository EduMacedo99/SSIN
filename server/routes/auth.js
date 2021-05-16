const Crypto = require('crypto');
const express = require('express')
let app = express.Router()
const net = require('net')
const symmetric = require('../symmetric_encryption')

/**
 * A client sends their username+token, and is asking to start a new session
 * If username+token exists, Authenticator Server sends a challenge (different each time)
 */
app.get('/', function (req, res) {
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
    const N = Crypto.randomBytes(32).toString('hex')
    // Encrypt challenge and save it on the BD
    const enc_challenge = symmetric.encrypt(N,  bd_iv, bd_symmetric_key)
    // TODO: ...

    // TODO: Protecting against replays needs a nonce or a timestamp, Timestamps need time synchronization which enlarges the attack surface
    // ... The challenge probably should have a challenge_lifetime that expires?

    res.status(200).json({"msg": username+ "? Prove it, challenge: " + N, challenge: N})

});

/**
 * Client challenge asnwer
 * If client is correct, refresh token
 */
app.get('/challengeRefreshToken', function (req, res) {
  const { msg, username, enc_challenge, port} = req.body
  console.log(" client<" + port + ">: " + msg)

  // Verify if is correct
  // Get symmetric key and encrypted challenge from BD
  // TODO: ... 
  const bd_symmetric_key = "wwiimwiegdgcyvdz"
  const bd_iv = "hsbkjbsmdpgdwfib"
  const bd_enc_challenge = ""
  // Encrypted challenge from BD must be equal to answer
  if(bd_enc_challenge != ""){//enc_challenge){
    res.status(500).json({"msg":"wrong answer."})
    return
  }

  // If so, distribute a short-term session key(new token) for being used between the two
  // Create new token
  const new_token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
          
  // Update BD with new token + port of client session
  // TODO: ...

  // Encrypt token
  const enc_token = symmetric.encrypt(new_token, bd_iv, bd_symmetric_key);

  // Send new token to the client
  res.status(200).json({"msg":"okay, it's a match.", token: enc_token})
  console.log("Authentication done.")

});

module.exports = app