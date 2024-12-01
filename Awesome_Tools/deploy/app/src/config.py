import os

class Config:
    UPLOAD_FOLDER = '/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024

    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DATABASE", "file_metadata")
    MYSQL_CURSORCLASS = 'DictCursor'
