import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = ?", session["user_id"])
    portfolio_value = 0

    # Extract Portfolio details
    portfolio_details = []
    for stock in stocks:
        symbol = stock["symbol"]
        shares = int(stock["shares"])
        price = lookup(symbol)["price"]
        total = round(price * shares, 2)

        # Format price and total
        price = "{:.2f}".format(price)
        total = "{:.2f}".format(total)

        # Gather portfolio details
        portfolio_value += float(total)  
        portfolio_details.append({
            'symbol': symbol,
            'shares': shares,
            'price': price,
            'total': total
        })

    # Extract user's cash and calculate their assets' value
    cash = round(db.execute("SELECT cash FROM users WHERE id = ?", 
                            session["user_id"])[0]["cash"], 2)
    assets = round(cash + portfolio_value, 2)
    
    # Format price and total 
    cash = "{:.2f}".format(cash)
    assets = "{:.2f}".format(assets)
    
    # Redirect user to home page
    return render_template("index.html", cash=cash, portfolio_details=portfolio_details, assets=assets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Make sure symbol is valid 
        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("invalid symbol", 400)

        # Extract required stock details
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", 
                          session["user_id"])[0]["cash"]
        symbol = lookup(symbol)["symbol"]
        price = lookup(symbol)["price"]

        # Make sure shares are are integers:
        # Get the value from the form
        input_shares = request.form.get("shares")

        # Check if the input contains a decimal point
        if '.' in input_shares:
            # Render an error message indicating that only integers are allowed
            return apology("Shares must be integers")

        # Convert to integer
        try:
            purchased_shares = int(input_shares)
        except ValueError:
            # Render an error message indicating that only integers are allowed
            return apology("Shares must be integers")

        total = price * purchased_shares

        # Make sure shares are positve
        if purchased_shares <= 0:
            return apology("Shares must be positve", 400)
        # Make sure user can afford stock
        total = price * purchased_shares
        if total > cash:
            return apology("can't afford stock", 400)

        # Purchase stock
        type = "buy"
        time = datetime.datetime.now()

        db.execute("INSERT INTO transactions (symbol, shares, type, time) VALUES (?, ?, ?, ?)", 
                   symbol, purchased_shares, type, time)
        transaction_id = db.execute("SELECT MAX(id) FROM transactions")[0]["MAX(id)"]
        db.execute("INSERT INTO transacted (user_id, transaction_id) VALUES (?, ?)", 
                   session["user_id"], transaction_id)
        
        owned_shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND SYMBOL = ?", 
                                  session["user_id"], symbol)
        if not owned_shares:
            db.execute("INSERT INTO stocks (user_id, symbol, shares) VALUES (?, ?, ?)", 
                       session["user_id"], symbol, purchased_shares)
        else:
            db.execute("UPDATE stocks SET shares = shares + ? WHERE user_id = ? AND symbol = ?", 
                       purchased_shares, session["user_id"], symbol)

        # Update user's cash
        cash = cash - total
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, session["user_id"])
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, type, time FROM transactions WHERE id IN (SELECT transaction_id FROM transacted WHERE user_id = ?)", session["user_id"])
    transaction_details = []
    for transaction in transactions:
        symbol = transaction["symbol"]
        print(symbol)
        type = transaction["type"]
        shares = int(transaction["shares"])
        time = transaction["time"]
        price = lookup(symbol)["price"]
        
        transaction_details.append({
            'symbol': symbol,
            'type': type,
            "shares": shares,
            "time": time,
            "price": "{:.2f}".format(price)
        })
    return render_template("history.html", transactions=transaction_details)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If symbol is invalid, retrun apology
        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("invalid symbol", 400)
        
        # If symbol is valid, return the stock quote of this symbol
        price = "{:.2f}".format(lookup(symbol)["price"])
        symbol = lookup(symbol)["symbol"]
        return render_template("quoted.html", symbol=symbol, price=price)
     
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")
    

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
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))       
        # Ensure username is available 
        if len(rows) > 0:
            return apology("Username is not available", 400)
        
        # Generate hash of the password
        hash = generate_password_hash(request.form.get("password"))
        # Insert user into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", 
                   request.form.get("username"), hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))       
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
 
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Make sure valid symbol exists
        if symbol == None or lookup(symbol) == None:
            return apology("missing symbol", 400)
        
         # Make sure sold shares are positve
        sold_shares = int(request.form.get("shares"))
        if sold_shares <= 0:
            return apology("Shares must be positve", 400)

        # Make sure sure user has enough shares to sell
        owned_shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND SYMBOL = ?", 
                                  session["user_id"], symbol)[0]["shares"]

        if sold_shares > owned_shares:
            return apology("Too many shares", 400)

        # Sell stock
        type = "sell"
        time = datetime.datetime.now()

        db.execute("INSERT INTO transactions (symbol, shares, type, time) VALUES (?, ?, ?, ?)", 
                   symbol, sold_shares, type, time)
        transaction_id = db.execute("SELECT MAX(id) FROM transactions")[0]["MAX(id)"]
        db.execute("INSERT INTO transacted (user_id, transaction_id) VALUES (?, ?)", 
                   session["user_id"], transaction_id)
        db.execute("UPDATE stocks SET shares = shares + - ? WHERE user_id = ? AND symbol = ?", 
                   sold_shares, session["user_id"], symbol)

        # Update user's cash
        price = "{:.2f}".format(lookup(symbol)["price"])
        total = sold_shares * float(price)
        cash = round(db.execute("SELECT cash FROM users WHERE id = ?", 
                                session["user_id"])[0]["cash"], 2)
        cash = cash + total
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, session["user_id"])
        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        symbol_dicts = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", session["user_id"])
        symbols = []
        for dict in symbol_dicts:
            symbol = dict["symbol"]
            symbols.append(symbol)
        return render_template("sell.html", symbols=symbols)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Increase or decrease user's cash."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Make sure required cash is within the allowed range.
        cash = int(request.form.get("cash"))
        if cash > 2000 or cash < -2000:
            return apology("Cash should be within -2000 to 2000", 400)
        else: 
            # Update user's cash
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?;", cash, session["user_id"])
            
            # Redirect user to home page
            return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html")