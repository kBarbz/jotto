from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
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

# Decorator function to require log-in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Show homepage with instructions and Start Game menu
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Login page and process **CS50 code**
@app.route("/login", methods=["GET", "POST"])
def login():
    # Set up use of database
    file = "./jotto-db"
    conn = sqlite3.connect(file)
    c = conn.cursor()

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
        c.execute("SELECT * FROM users WHERE username =:username", {"username": request.form.get("username")})
        user = c.fetchone()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user[2], request.form.get("password")):
            return render_template("error.html", error_desc = "Incorrect username or password")

        # Remember which user has logged in
        session["user_id"] = user[1]
        conn.close()

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

        # Set up use of database
        file = "./jotto-db"
        conn = sqlite3.connect(file)
        c = conn.cursor()

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error_desc = "Empty username field")

        # Ensure question was selected and answer was submitted
        elif not request.form.get("answer"):
            return render_template("error.html", error_desc = "Empty secret question answer field")
        elif not request.form.get("question"):
                return render_template("error.html", error_desc = "Empty secret question answer field")

        # Ensure passwords were submitted
        elif not request.form.get("password"):
            return render_template("error.html", error_desc = "Empty password field")
        elif not request.form.get("confirmation"):
            return render_template("error.html", error_desc = "Empty confirmation field")

        # Create hashof password and answer based on users input
        pass_hash = generate_password_hash(request.form.get("confirmation"))
        answer = request.form.get("answer").lower()

        # Check to see if username is valid and update users password in database
        result = c.execute("INSERT INTO users (username, hash, question, answer) VALUES (:username, :hash, :question, :answer)",
                  {"username": request.form.get("username"), "hash": pass_hash, "question": request.form.get("question"), "answer": answer})
        conn.commit()
        if not result:
            return render_template("error.html", error_desc = "Invalid username")
        else:
            c.execute("SELECT id FROM users WHERE username =:username", {"username": request.form.get("username")})
            user = c.fetchone()
            session["user_id"] = user[0]
            conn.close()
            return redirect("/")

    else:
        return render_template("register.html")

# Change password while logged in
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # Set up use of database
    file = "./jotto-db"
    conn = sqlite3.connect(file)
    c = conn.cursor()

    if request.method == "POST":
        c.execute("SELECT hash FROM users where id=:id", {"id": session["user_id"]})
        user_hash = c.fetchone()

        # Ensure passwords were submitted
        if not request.form.get("old_password"):
            return render_template("error.html", error_desc = "Empty old password field")
        elif not request.form.get("new_password"):
            return render_template("error.html", error_desc = "Empty new password field")
        elif not request.form.get("confirmation"):
            return render_template("error.html", error_desc = "Empty confirmation field")

        # Check if passwords match
        if request.form.get("new_password") != request.form.get("confirmation"):
            return render_template("error.html", error_desc = "Passwords don't match")

        # Check if it's the correct password
        if not check_password_hash((user_hash[0]), request.form.get("old_password")):
            return render_template("error.html", error_desc = "Old password incorrect")
        else:
            pass_hash = generate_password_hash(request.form.get("confirmation"))
            c.execute("UPDATE users SET hash =:hash WHERE id =:id", {"hash": pass_hash, "id": session["user_id"]})
            conn.commit()
            conn.close()

        return redirect('/')
    else:
        return render_template("change_password.html")

# Change password using Security Question
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    # Set up use of database
    file = "./jotto-db"
    conn = sqlite3.connect(file)
    c = conn.cursor()

    if request.method == "POST":

        # Ensure all fields were submitted
        if not request.form.get("username"):
            return render_template("error.html", error_desc = "Empty username field")
        elif not request.form.get("answer"):
            return render_template("error.html", error_desc = "Empty answer field")
        elif not request.form.get("new_password"):
            return render_template("error.html", error_desc = "Empty new password field")
        elif not request.form.get("confirmation"):
            return render_template("error.html", error_desc = "Empty confirmation field")

        # Check if passwords match
        if request.form.get("new_password") != request.form.get("confirmation"):
            return render_template("error.html", error_desc = "Passwords don't match")

        # Get users details
        c.execute("SELECT * FROM users WHERE username =:username", {"username": request.form.get("username")})
        user = c.fetchone()

        # Check if answer is correct and update password
        if user[4] == request.form.get("answer").lower():
            pass_hash = generate_password_hash(request.form.get("confirmation"))
            c.execute("UPDATE users SET hash =:hash WHERE id=:id", {"hash": pass_hash, "id": user[0]})
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            return render_template("error.html", error_desc = "Incorrect answer")

    else:
        return render_template("reset_password.html")

@app.route("/check_question", methods=["GET"])
def check_question():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")

    # Set up use of database
    file = "./jotto-db"
    conn = sqlite3.connect(file)
    c = conn.cursor()

    c.execute("SELECT question FROM users WHERE username = :username", {"username": username})
    question = c.fetchone()
    if not question:
        return jsonify("Input correct username")
    if question[0] == "pet":
        q = "Name of your first pet?"
    elif question[0] == "maiden":
        q = "Mother's maiden name?"
    elif question[0] == "friend":
        q = "Best friend's name?"
    elif question[0] == "tv":
        q = "Favourite TV Show?"
    elif question[0] == "middle":
        q = "Your middle name?"
    return jsonify(q)

@app.route("/check_login", methods=["GET"])
def check_login():

    # Get arguments from GET request
    username = request.args.get("username")

    # Set up use of database
    file = "./jotto-db"
    conn = sqlite3.connect(file)
    c = conn.cursor()

    # Grab users details
    c.execute("SELECT * FROM users where username = :username", {"username": username})
    user = c.fetchone()

    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)
