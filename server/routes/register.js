const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
let app = express.Router()

const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')
const DB = require("../DBconnect.js")


app.get('/', function (req, res) {
    //console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {

    console.log("\nStart of Registration ...")

    const enc_ID = req.body.ID_encrypt;
    const enc_iv = req.body.encrypt_iv;
    const enc_key = req.body.encrypt_key;
    const username = req.body.username;
 
    //console.log("ID: " + enc_ID);
    //console.log("iv: " + enc_iv)
    //console.log("key: " + enc_key)

    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');

    console.log("... decrypting request")
    
    const onetimeID = privateKey.decrypt(forge.util.decode64(enc_ID), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    const iv = privateKey.decrypt(forge.util.decode64(enc_iv), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    const symmetric_key = privateKey.decrypt(forge.util.decode64(enc_key), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    //console.log("ID: " + onetimeID);
    //console.log("key: " + symmetric_key);
    //console.log("iv: " + iv);

    // TODO: confirmar na BD que o cliente onetimeID é correto
    // na bd está com um hash de sha256
    console.log("... verifying if one time ID and username are valid")

    //criar um token
    const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
    console.log("... new token: " + token)

    const enc_token = symmetric.encrypt(token, iv, symmetric_key);
    //console.log("enc_token: " + enc_token);
    res.json({
        'token': enc_token,
    });

    // TODO: se encriptarmos o token, como depois podemos verificá-lo sem o mesmo iv?
    // Save token and symmetric key in DB
    console.log("... saving new token and symmetric key in DB")
    DB.saveClientRegistration(username, token, symmetric_key);
    console.log("Registration done.\n")

});

module.exports = app
