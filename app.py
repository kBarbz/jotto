from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Configure application **CS50 code**
app = Flask(__name__)

# Ensure templates are auto-reloaded **CS50 code**
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached **CS50 code**
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies) **CS50 code**
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up use of database
file = "jotto-db"
conn = sqlite3.connect(file)
c = conn.cursor()


# Show homepage with instructions and Start Game menu
@app.route("/")
def index():
    return render_template("index.html")

# Login page and process **CS50 code**
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error_desc = "Empty username field")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", error_desc = "Empty password field")

        # Query database for username
        user = c.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", error_desc = "Failed finding user")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout and return to login screen.
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Register as a user
@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error_desc = "Empty username field")

        elif not request.form.get("answer"):
            return render_template("error.html", error_desc = "Empty secret question answer field")

        # Ensure passwords were submitted
        elif not request.form.get("password"):
            return render_template("error.html", error_desc = "Empty password field")

        elif not request.form.get("pass-confirmation"):
            return render_template("error.html", error_desc = "Empty confirmation field")

            
        return redirect("/")
    else:
        return render_template("register.html")
