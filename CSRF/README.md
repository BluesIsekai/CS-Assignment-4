# GET-based forged action (CSRF)

**Owner: Saqlain · IIT2024113**

This is a separate local application in the group's existing `CSRF` folder.
It changes only a disposable in-memory email address. Both servers bind to loopback.
Restarting the victim server discards accounts and generates a new signing key.

## Run

From the repository's `CSRF` directory, using Python 3.10 or later:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

In a second terminal in the same directory:

```powershell
.\.venv\Scripts\python.exe attacker.py
```

Alternatively, after installing dependencies, run `./start_demo.ps1` in PowerShell.
If local execution policy blocks it, use the two Python commands above.
Stop the servers with Ctrl+C.

Victim: **http://127.0.0.1:5000/**. Attacker: **http://localhost:8001/**.
Keep these hostnames exactly as written. Different ports alone create different
origins, but do not necessarily create different sites. `localhost` versus
`127.0.0.1` makes this a cross-site demonstration. Both resolve to your computer.

## (a) Vulnerable implementation

In `app.py`, `change_email()` accepts a GET in vulnerable mode and changes the
server-side record using the `email` query parameter. The login session cookie
identifies the victim, but the handler requires no proof that the victim intended
this particular change. The dashboard explicitly labels this mode VULNERABLE.
`/login` selects a seeded demo identity; it is not production authentication.

## (b) Working exploit and evidence procedure

1. Open the victim URL and click **Log in as Saqlain**.
2. Click **Reset → vulnerable**. Show `saqlain@example.test`.
3. Open the attacker URL in the same browser profile. Click **Claim reward**.
4. The browser navigates to the victim; the email becomes `attacker@example.test`.
5. Capture the dashboard as `screenshots/01_vulnerable_changed.png`.
6. Click **Reset → secure**. The email resets to the original value.
7. Reopen the attacker page and click the **same unchanged link**.
8. Show **Request blocked**, HTTP **405** in the browser Network panel, and capture
   `screenshots/02_secure_blocked.png`.
9. Click **Return to account and verify email**. It remains `saqlain@example.test`.
   Capture `screenshots/03_secure_unchanged.png`.
10. Use the legitimate secure form to save `saqlain.updated@example.test` and show
    that an intended update still works.

Exact payload in `templates/attacker.html`:

```html
<a href="http://127.0.0.1:5000/change-email?email=attacker%40example.test">Claim reward</a>
```

Request sent by the browser (the attacker does not know the cookie value):

```http
GET /change-email?email=attacker%40example.test HTTP/1.1
Host: 127.0.0.1:5000
Cookie: csrf_lab=<victim browser's existing session cookie>
```

This is a **top-level navigation**, not an image request. `SameSite=Lax` permits
cookies on cross-site top-level GET navigations, so the attack is reproducible
without weakening the browser's cookie defaults. An image-based cross-site
payload would generally lose Lax cookies and would not demonstrate this reliably.

## (c) Root cause

The application treats an authenticated, state-changing GET as proof of user
intent. A different site can trigger that navigation while the browser supplies
the victim's existing login cookie automatically.

## (d) Mitigation implemented

The primary fix is **avoiding state-changing GET requests**. Secure mode returns
405 with `Allow: POST` for the identical forged URL before changing the email.
The legitimate form uses POST. It additionally carries a cryptographically random
synchronizer token stored in the server-side demo record, compared using
`secrets.compare_digest`. Missing, incorrect, or another session's token returns
403. This additional check matters because changing GET to POST alone cannot
prevent an attacker from submitting a cross-origin POST form.

The same endpoint, session, cookie policy, and exact attacker payload are used
before and after the fix. No query parameter can switch mitigation off; only a
token-protected local configuration form changes the mode. HEAD never changes
the email in either mode. UI output is escaped by Jinja.

## (e) Other mitigations / viva theory

**Synchronizer tokens** bind an unpredictable request value to the user's session;
another site can submit requests but cannot read that token under the same-origin
policy. This lab also implements that protection for POST. **SameSite cookies**
restrict cross-site cookie attachment: Strict is stronger but affects incoming
links; Lax still permits top-level GET navigations, which explains why this lab's
exploit works. **Re-authentication** asks for fresh proof of identity before a
sensitive action; it must be bound to the action and properly protected rather
than trusting an already logged-in session. **Avoiding state-changing GETs** keeps
read-only navigation from performing actions; it should accompany token protection
for writes. HttpOnly prevents JavaScript from reading a cookie but does not stop
the browser attaching it. CORS primarily limits reading cross-origin responses;
it does not block this navigation. Neither is sufficient protection against CSRF.

Reference: [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_app
```

Nine request-level tests cover vulnerable success, identical-payload rejection,
valid and invalid tokens, session isolation, authentication, reset protection,
read-only HEAD handling, and the exact attacker link. These tests do not simulate
browser SameSite enforcement. The browser procedure above describes how to verify
the cross-site navigation and capture exploit and mitigation evidence.
