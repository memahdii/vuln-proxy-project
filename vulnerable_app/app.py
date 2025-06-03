from flask import Flask, request
import sqlite3

app = Flask(__name__)


# Initialize a SQLite DB with one user
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    # Create 'users' table if it doesn't exist
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    # Insert a default user
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    conn.commit()
    conn.close()


# Login endpoint vulnerable to SQL Injection
@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # VULNERABLE: User input directly embedded into SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing query:", query)

    result = c.execute(query).fetchall()
    conn.close()

    if result:
        return "Login successful"
    else:
        return "Login failed"


# In-memory list to store comments
comments = []


# Comment form vulnerable to stored XSS
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        text = request.form.get("text", "")
        comments.append(text)  # No sanitization or escaping
    # VULNERABLE: Unescaped user input rendered directly in HTML
    return "<h1>Comments</h1>" + "<br>".join(comments) + '''
        <form method="post">
            <input name="text">
            <input type="submit">
        </form>
    '''


# Start the app after setting up the DB
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

