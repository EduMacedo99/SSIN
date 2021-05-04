const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
let app = express.Router()

app.get('/', function (req, res) {
    console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    console.log(req.body.token);
    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    
    const onetimeID = privateKey.decrypt(forge.util.decode64(req.body.token), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
    console.log(onetimeID);
    console.log(req.body.encrypt_pass);
    //confirmar na BD que cliente onetimeID é correto
    //criar um token
    const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
    //guardar na DB
    //encriptar com chave simétrica -> append 16 bytes to IV
    
    //enviar token para o cliente
    res.json({'token': token});
});

module.exports = app

//encrypt and decrypt with AES-CBC

// 'use strict';

// const crypto = require('crypto');
// const ENC_KEY = "bf3c199c2470cb477d907b1e0917c17b"; // set random encryption key
// const IV = "5183666c72eec9e4"; // set random initialisation vector
// // ENC_KEY and IV can be generated as crypto.randomBytes(32).toString('hex');

// const phrase = "who let the dogs out";

// var encrypt = ((val) => {
//   let cipher = crypto.createCipheriv('aes-256-cbc', ENC_KEY, IV);
//   let encrypted = cipher.update(val, 'utf8', 'base64');
//   encrypted += cipher.final('base64');
//   return encrypted;
// });

// var decrypt = ((encrypted) => {
//   let decipher = crypto.createDecipheriv('aes-256-cbc', ENC_KEY, IV);
//   let decrypted = decipher.update(encrypted, 'base64', 'utf8');
//   return (decrypted + decipher.final('utf8'));
// });



// encrypted_key = encrypt(phrase);
// original_phrase = decrypt(encrypted_key);