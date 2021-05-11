const crypto = require('crypto');
const express = require('express')
let app = express.Router()
const net = require('net');

/**
 * A client sends their username and ip+port, and is asking to start a new session
 * If username exists, Authenticator Server sends a challenge (different each time)
 * The server waits for the client asnwer in the new client channel
 * If client is correct, refresh token
 */
app.get('/', function (req, res) {
    console.log("\nStart authentication...");
    const username = req.body.username;
    const port = req.body.port;

    // Check if username exists on the BD
    // TODO: ...

    // Generate a unique random value
    const N = crypto.randomBytes(32).toString('hex');

    // TODO: Protecting against replays needs a nonce or a timestamp, Timestamps need time synchronization which enlarges the attack surface
    // ... The challenge probably should have a challenge_lifetime that expires?

    res.status(200).json({"text": "hmm " + username+ "? Prove it :)\n I will be waiting on port " + port, "challenge": N})

    // Create a channel to talk with client
    const server = net.createServer((socket) => {
        console.log("Client connection from (", socket.remoteAddress, ", ", socket.remotePort, ")")
      
        socket.on("data", (buffer) => {
          console.log("Got your answer :/ ")

          // Verify if is correct
          // TODO: ...

          // If so, distribute a short-term session key(new token) for being used between the two
          // Create new token
          // TODO: ...
          
          // Update BD
          // TODO: ...

          // Encrypt token
          // TODO: ...

          // Send new token to the client
          // TODO: ...
          socket.write("dont know yet")

        });

        socket.on("end", () => {
          console.log("Authentication connection ended...")
        });
      });

    // TODO: it's necessary to initialize a new thread?  
    server.listen(port);

});

module.exports = app