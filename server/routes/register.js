const fs = require('fs');
var sha256 = require('js-sha256');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
const DB = require('../DBconnect');
let app = express.Router()
const utils = require("../utils")
const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')


function assymetric_decrypt (message){
    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    return privateKey.decrypt(forge.util.decode64(message), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
}

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
 
    // console.log("ID: " + enc_ID);
    // console.log("iv: " + enc_iv)
    // console.log("key: " + enc_key)
    
    const onetimeID = assymetric_decrypt(enc_ID);
    const iv = assymetric_decrypt(enc_iv);
    const symmetric_key = assymetric_decrypt(enc_key);
    // console.log("ID: " + onetimeID);
    // console.log("username: " + username);
    // console.log("key: " + symmetric_key);
    // console.log("iv: " + iv);
    console.log("... checking if username and one time id macthes DB.")

    const sql_confirm_ID = "SELECT one_time_id FROM users WHERE username=?"
    DB.db.get(sql_confirm_ID, [username], (err, row) => {
        if (err) {
            console.log("Error accessing database")
            return;
        } 
        else if (row == undefined) {
            res.statusCode = 404;
            res.json({
                'message': 'User not found',
            });
            return;
        }
        else {

            let onetimeIdHash = sha256(onetimeID)
            //console.log("SQL > " + row.one_time_id + '\n > Client > ' + sha256(onetimeID))
            if (row.one_time_id != onetimeIdHash) {
                res.statusCode = 401;
                res.json({
                    'message': 'Wrong one_time _ID',
                });
                return;
            }
            else {
                console.log("... valid username and one time id.")

                //criar um token
                const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
                console.log("... token: " + token)
                //**************************************************************************** */
               
                //TODO -> criar um novo iv e enviá-lo juntamente com o enc_token
                const enc_token = symmetric.encrypt(token, iv, symmetric_key);
                //console.log("... enc_token: " + enc_token);
                res.statusCode = 200;
                res.json({
                    'token': enc_token,
                });
                console.log("... saving new token and symmetric key in DB")
                utils.saveClientRegistration(username, token, symmetric_key);
                console.log("Registration done.\n")
            }  
        };
    });
});

module.exports = app
