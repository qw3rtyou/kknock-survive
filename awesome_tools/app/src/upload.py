from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
    current_app,
)
from werkzeug.utils import secure_filename
from models import mysql
from auth import login_required
import os


file_bp = Blueprint("file_bp", __name__)


@file_bp.route("/upload", methods=["GET"])
@login_required
def upload():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT filename FROM files")
    files = cursor.fetchall()
    return render_template("file/upload.html", files=files)


@file_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        return redirect(url_for("file_bp.upload"))
    files = request.files.getlist("file")
    for file in files:
        if file.filename == "":
            continue
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO files (filename, filepath) VALUES (%s, %s)",
            (filename, os.path.join(current_app.config["UPLOAD_FOLDER"], filename)),
        )
        mysql.connection.commit()
    return redirect(url_for("file_bp.upload"))


@file_bp.route("/download/<filename>", methods=["GET"])
@login_required
def download_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@file_bp.route("/delete/<filename>", methods=["GET"])
@login_required
def delete_file(filename):
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        cursor = mysql.connection.cursor()
        cursor.execute(f"DELETE FROM files WHERE filename = '{filename}'")
        mysql.connection.commit()

    return redirect(url_for("file_bp.upload"))
