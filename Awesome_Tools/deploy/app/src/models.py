from flask_mysqldb import MySQL
import os
from datetime import datetime

mysql = MySQL()

def init_db(app):
    mysql.init_app(app)
    with app.app_context():
        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                filepath VARCHAR(255) NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user'
            )
            """
        )
        
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin')

        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, 'admin')
            ON DUPLICATE KEY UPDATE password = %s, role = 'admin';
            """,
            (admin_username, admin_password, admin_password)
        )

        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES ('test', 'test', 'admin')
            ON DUPLICATE KEY UPDATE password = 'test', role = 'admin';
            """
        )

        uploads_dir = '/uploads'
        for filename in os.listdir(uploads_dir):
            if os.path.isfile(os.path.join(uploads_dir, filename)):
                filepath = os.path.join(uploads_dir, filename)
                cursor.execute(
                    "INSERT INTO files (filename, filepath, upload_time) VALUES (%s, %s, %s);",
                    (filename, filepath, datetime.now())
                )

        mysql.connection.commit()


def create_user(username, password, role='user'):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role),
    )
    mysql.connection.commit()


def delete_user(username):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    mysql.connection.commit()