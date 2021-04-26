const fs = require('fs');
const forge = require('node-forge');
const express = require('express');
let app = express.Router()

app.get('/', function (req, res) {
    console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    console.log(req.body.token);
    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    
    const token = privateKey.decrypt(forge.util.decode64(req.body.token), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
        md: forge.md.sha1.create()
        }
    });
    console.log(token);
    res.json({'ok':'ok'});
});

module.exports = app