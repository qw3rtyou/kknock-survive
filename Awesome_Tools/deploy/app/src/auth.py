from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from functools import wraps
from models import mysql

auth_bp = Blueprint('auth_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "role" not in session or session.get("role") != "admin":
            flash("You do not have permission to access this page.")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/profile")
@login_required
def profile():
    username = session.get("username")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        return render_template("profile.html", user=user)
    else:
        flash("User not found.")
        return redirect(url_for("index"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and user["password"] == password:
            session["logged_in"] = True
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for("auth_bp.login"))



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("auth_bp.register"))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash("Username already exists")
            return redirect(url_for("auth_bp.register"))
        else:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                           (username, password, "user"))
            mysql.connection.commit()
            flash("Account created successfully. You can now log in.")
            return redirect(url_for("auth_bp.login"))

    return render_template("register.html")