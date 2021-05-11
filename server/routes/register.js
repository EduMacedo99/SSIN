const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
let app = express.Router()

const crypto = require('crypto') 
const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')

app.get('/', function (req, res) {
    console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    const iv = req.body.iv;
    const key = req.body.key;
 
    console.log(req.body.token);
    console.log(req.body.encrypt_pass)
    console.log(req.body.cenas)
    const cenas_dec = symmetric.decrypt(req.body.cenas, iv, key)
    console.log("decript: "+ cenas_dec)
    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    
    const onetimeID = privateKey.decrypt(forge.util.decode64(req.body.token), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    const symmetric_key = privateKey.decrypt(forge.util.decode64(req.body.encrypt_pass), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    console.log("ID: " + onetimeID);
    console.log("pass: " + symmetric_key);
    //confirmar na BD que cliente onetimeID é correto
    //criar um token
    const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
    console.log("token: " + token)
    //**************************************************************************** */
    
    
    const enc_token = symmetric.encrypt(token, iv, key)

    console.log("enc_token: " + enc_token)
    
    res.json({'token': enc_token});

});

module.exports = app
