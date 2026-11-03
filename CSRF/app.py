"""Saqlain IIT2024113 — local GET-based CSRF teaching lab."""
import secrets
from functools import wraps

from flask import Flask, abort, redirect, render_template, request, session, url_for

INITIAL_EMAIL = "saqlain@example.test"
FORGED_EMAIL = "attacker@example.test"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=secrets.token_hex(32), SESSION_COOKIE_NAME="csrf_lab",
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
    if test_config:
        app.config.update(test_config)
    # Local, disposable server-side records; restarting resets all demo accounts.
    records = {}

    def current():
        return records.get(session.get("demo_id"))

    def authenticated(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if current() is None:
                abort(401, description="Log into the demo first.")
            return view(*args, **kwargs)
        return wrapped

    def require_token():
        supplied = request.form.get("csrf_token", "")
        if not secrets.compare_digest(supplied, current()["token"]):
            abort(403, description="Blocked: missing or invalid anti-CSRF token.")

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/")
    def index():
        return render_template("dashboard.html", account=current())

    @app.post("/login")
    def login():
        # An explicit seeded demo identity, not a production authentication system.
        if current() is None:
            session.clear()
            demo_id = secrets.token_urlsafe(32)
            session["demo_id"] = demo_id
            records[demo_id] = dict(email=INITIAL_EMAIL, mode="vulnerable",
                                    token=secrets.token_urlsafe(32), events=[])
        return redirect(url_for("index"), code=303)

    @app.post("/configure")
    @authenticated
    def configure():
        require_token()
        mode = request.form.get("mode")
        if mode not in ("vulnerable", "secure"):
            abort(400)
        account = current()
        account.update(mode=mode, email=INITIAL_EMAIL, events=[])
        return redirect(url_for("index"), code=303)

    @app.route("/change-email", methods=["GET", "POST"])
    @authenticated
    def change_email():
        account = current()
        # MITIGATION: reject state-changing GET/HEAD, then verify POST intent.
        # Both modes use the SAME URL so the exact forged payload can be replayed.
        if request.method == "HEAD" or (account["mode"] == "secure" and request.method != "POST"):
            account["events"].append("BLOCKED: GET/HEAD email change (405)")
            response = app.make_response((render_template("blocked.html", reason="GET cannot change the email. Use the legitimate POST form with its anti-CSRF token."), 405))
            response.headers["Allow"] = "POST"
            return response
        if account["mode"] == "secure":
            require_token()
        # VULNERABLE PATH: GET input plus ambient login cookie is enough to mutate.
        email = request.args.get("email", "") if request.method == "GET" else request.form.get("email", "")
        if len(email) > 120 or "@" not in email or any(c in email for c in "\r\n"):
            abort(400, description="Enter a demo email address.")
        account["email"] = email
        account["events"].append(f"CHANGED via {request.method}: {email}")
        return redirect(url_for("index"), code=303)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("blocked.html", reason=error.description), 403

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
