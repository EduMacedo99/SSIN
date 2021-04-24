import express from "express";
import auth from './routes/auth';
import service from './routes/service';
import register from './routes/register.js';
import coms from './routes/coms';

const app = express();
const port = 3000;

app.use('/register', register);
app.use('/auth', auth)
app.use('/service', service);
app.use('/coms', coms);

app.listen(port, () =>
  console.log(`Hello world app listening on port ${port}!`)
);