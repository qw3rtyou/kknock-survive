const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8888;
const FLAG = process.env.FLAG || "FLAG{example_flag}";

const USERS = {
    "admin": {
        "username": "admin",
        "password": require('crypto').randomBytes(16).toString('hex'),  //Do not bruteforce!!
    },
    "guest": {
        "username": "guest",
        "password": "guest",
    }
};

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.urlencoded({ extended: false }));

app.get("/", (req, res) => {
    res.render('index');
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;
    const user = USERS[username];

    if (user) {
        if (username == "guest") {
            res.render('result', { msg: `Welcome, Guest` });
        } else {
            res.render('result', { msg: `Welcome, ${username}. ${FLAG}` });
        }
    } else {
        res.render('result', { msg: `Invalid username or password` });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
