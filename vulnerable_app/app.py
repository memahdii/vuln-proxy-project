from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Set up a basic in-memory DB
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    c.execute("INSERT INTO users (username, password) VALUES ('mahdi', 'mahdipass')")
    c.execute("INSERT INTO users (username, password) VALUES ('igor', 'igorpass')")
    conn.commit()
    conn.close()

@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing query:", query)
    result = c.execute(query).fetchall()
    conn.close()
    if result:
        return "Login successful"
    else:
        return "Login failed"


comments = []

@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        text = request.form.get("text", "")
        comments.append(text)
    return "<h1>Comments</h1>" + "<br>".join(comments) + '''
        <form method="post">
            <input name="text">
            <input type="submit">
        </form>
    '''

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
