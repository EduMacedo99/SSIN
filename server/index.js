const express = require("express");
const auth = require('./routes/auth')
const app = express();
const port = 3000;


app.use('/auth', auth)

app.listen(port, () =>
  console.log(`Hello world app listening on port ${port}!`)
);