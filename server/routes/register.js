const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
let app = express.Router()

const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')

/**
* Save token, symmetric key, symmetric key iv in DB
*/
/*function saveClientRegistration (username, token, symmetric_key, symmetric_key_iv) {
    // Update DB
    const sql = "UPDATE users SET token=?, symmetric_key=?, symmetric_key_iv=? WHERE username=?"
    db.run(sql, [token, symmetric_key, symmetric_key_iv, username], (err, row) => {
        if (err) 
            return console.error(err.message)
        if (row) 
            console.log("Updated DB client: ", row)
    });
}*/

app.get('/', function (req, res) {
    console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    const enc_ID = req.body.ID_encrypt;
    const enc_iv = req.body.encrypt_iv;
    const enc_key = req.body.encrypt_key;
 
    console.log("ID: " + enc_ID);
    console.log("iv: " + enc_iv)
    console.log("key: " + enc_key)

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
    // TODO: confirmar na BD que cliente onetimeID é correto
    //criar um token
    const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
    console.log("token: " + token)
    //**************************************************************************** */
    
    // Save token, symmetric key, symmetric key iv in DB
    // TODO: test this 
    /*saveClientRegistration(username, token, symmetric_key, iv);*/
    
    const enc_token = symmetric.encrypt(token, iv, symmetric_key);
    console.log("enc_token: " + enc_token);
    res.json({
        'token': enc_token,
    });

});

module.exports = app
