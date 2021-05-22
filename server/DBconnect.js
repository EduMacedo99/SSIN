const sqlite3 = require('sqlite3');

/**
* Open the database
*/
let db = new sqlite3.Database('../database/Database.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    else console.log('Connected to database.');
  });


/**
* Save token and symmetric key in DB
*/
function saveClientRegistration (username, token, symmetric_key) {
  const sql = "UPDATE users SET token=?, symmetric_key=? WHERE username=?"
  db.run(sql, [token, symmetric_key, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  });
}

/**
* Save challenge and their expire timeout on the DB
*/
function saveChallenge (username, challenge, timeout) {
  const sql = "UPDATE users SET challenge=?, challenge_timeout=? WHERE username=?"
  db.run(sql, [challenge, timeout, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  })
}

/**
* Save new token and ip_port of client session
*/
function saveClientNewSession (username, token, ip_port) {
    const sql = "UPDATE users SET token=?, ip_address=? WHERE username=?"
    db.run(sql, [token, ip_port, username], async function (err, row) {
      if (err) {
        return console.error(err.message);
      }
    })
}

module.exports = {
  db,
  saveClientRegistration,
  saveChallenge,
  saveClientNewSession
}