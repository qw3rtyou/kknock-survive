const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8888;

const USERS = {
    "admin": {
        "username": "admin",
        "password": require('crypto').randomBytes(16).toString('hex'),  // Do not bruteforce!!
    },
    "guest": {
        "username": "guest",
        "password": "guest",
    }
};

const stat = {};

function isObject(obj) {
    return obj !== null && typeof obj === 'object';
}

function merge(a, b) {
    for (let key in b) {
        if (isObject(a[key]) && isObject(b[key])) {
            merge(a[key], b[key]);
        } else {
            a[key] = b[key];
        }
    }
    return a;
}

app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    res.render('index');
});

app.post("/login", (req, res) => {
    var hi = {}
    const { username, password } = req.body;
    const user = USERS[username];

    if (user) {
        if (username == "guest") {
            res.render('result', { msg: `Welcome, Guest` });
        } else if (username == "admin") {
            res.render('result', { msg: `Hehe no admin for U :)` });
        } else {
            merge(hi, req.body);
            res.render('render', { title: 'what?' });
        }
    } else {
        res.render('result', { msg: `Invalid username or password` });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
