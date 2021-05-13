const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
let app = express.Router()

const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')

app.get('/', function (req, res) {
    console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    const enc_ID = req.body.ID_encrypt;
    const enc_iv = req.body.encrypt_iv;
    const enc_key = req.body.encrypt_key;
    const enc_message = req.body.message;
 
    console.log("ID: " + enc_ID);
    console.log("iv: " + enc_iv)
    console.log("key: " + enc_key)
    console.log("message: " + enc_message);

    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    
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
    console.log("ID: " + onetimeID);
    console.log("key: " + symmetric_key);
    console.log("iv: " + iv);
    //confirmar na BD que cliente onetimeID é correto
    //criar um token
    const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
    console.log("token: " + token)
    //**************************************************************************** */
    
    const decrypt_message = symmetric.decrypt(enc_message, iv, symmetric_key);
    const enc_token = symmetric.encrypt(token, iv, symmetric_key);
    console.log("message: " + decrypt_message);
    console.log("enc_token: " + enc_token);
    const final_message = symmetric.encrypt(decrypt_message, iv, symmetric_key);
    res.json({
        'token': enc_token,
        'final_message': final_message,
    });

});

module.exports = app
