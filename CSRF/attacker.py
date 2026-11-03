"""Separate local origin: serve only the group's demonstration payload."""
from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("attacker.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=False)
