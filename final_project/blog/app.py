
"""
This web application was inspired by ChatGPT and the distribution code of the "finance" problem.
ChatGPT provided insights and guidance during the development process.
"""
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure upload folder
images_folder = 'static/images'
app.config['images_folder'] = images_folder

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blog.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/")
@login_required
def index():
    """Show latest posts"""
    
    latest_posts = db.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.time DESC
        LIMIT 9
    """)  

    return render_template("index.html", posts=latest_posts)


@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    """Write new post"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for title
        title = request.form.get("title")
        if not title:
            return apology("Must provide title", 400)

        elif len(title) < 4 or len(title) > 64:
            return apology("Title's length should be within 4 to 64 charactars", 400)
        
        # Check for subject
        body = request.form.get("body")
        if not body:
            return apology("Must provide body", 400)

        elif len(body) < 8 or len(body) > 1024:
            return apology("Body's length should be within 8 to 1024 charactars", 400)

        # Check for image and store  it if exists
        image = request.files.get("image")
        image_path = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['images_folder'], filename)
            image.save(image_path)


        # Get the current time
        time = datetime.now()

        # Save post in the database
        db.execute("INSERT INTO posts (user_id, title, image_path, body, time) VALUES (?, ?, ?, ?, ?)", session['user_id'], title, image_path, body, time)

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("create_post.html")

if __name__ == '__main__':
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    app.run(debug=True)


@app.route("/posts/<int:post_id>")
@login_required
def get_post(post_id):
    post = db.execute(
        """SELECT posts.*, users.username
        FROM posts 
        JOIN users ON posts.user_id = users.id 
        WHERE posts.id = ?
        """, post_id
        )

    if not post:
        return apology("Post not found", 400)

    post = post[0] 

    return render_template("post.html", post=post)

    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
   
        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        
        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))       
        # Ensure email is available 
        if len(rows) > 0:
            return apology("Email is not available", 400)
        
        # Generate hash of the password
        hash = generate_password_hash(request.form.get("password"))
        # Insert user into database
        db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", 
                   request.form.get("username"), request.form.get("email"), hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))       
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
