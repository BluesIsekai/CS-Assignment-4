# CommentHub — Stored XSS Demonstration

A local-only educational project showing **Stored Cross-Site Scripting (XSS)** and one mitigation: safe DOM rendering with `textContent`.

## What this demonstrates

- **Vulnerable Mode:** comments are retrieved from MySQL and rendered using `innerHTML`. This intentionally unsafe output sink can interpret attacker-controlled HTML.
- **Secure Mode:** the same records are rendered using `createElement`, `textContent`, and `appendChild`. Previously stored malicious-looking text is displayed as text and does not execute.
- Both modes use parameterized SQL queries. The database layer is not intentionally vulnerable to SQL injection.

The included test is a harmless browser alert using an image error handler. It does not collect credentials or transmit data.

## Requirements

- Node.js 18 or newer
- MySQL Server 8 or compatible
- npm

## Setup

1. Create the database and table by running `database/schema.sql` in MySQL Workbench or the MySQL command line:

   ```bash
   mysql -u root -p < database/schema.sql
   ```

2. Install dependencies from the project folder:

   ```bash
   npm install
   ```

3. Copy `.env.example` to `.env` and enter your local MySQL settings:

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=xss_demo
   PORT=3000
   ```

4. Start the app:

   ```bash
   npm start
   ```

5. Open `http://127.0.0.1:3000` in your browser.

## Demonstration steps

1. Open **Vulnerable Mode**.
2. Enter a display name and this harmless test comment:

   ```html
   <img src=x onerror="alert('Stored XSS executed!')">
   ```

3. Submit. The alert should appear. Refresh the page; the saved record is fetched from MySQL and rendered again, so the alert should appear again.
4. Open MySQL and run:

   ```sql
   USE xss_demo;
   SELECT id, username, comment, created_at FROM comments ORDER BY id DESC;
   ```

   This shows the payload stored as comment data.
5. Open **Secure Mode**. The same stored comment is displayed as literal text and does not execute.
6. Submit the same test comment in Secure Mode. It should also appear as text.

## Files to explain in your viva

- `frontend/js/vulnerable.js`: intentional vulnerable rendering sink (`innerHTML`).
- `frontend/js/secure.js`: mitigation using `textContent` and safe DOM methods.
- `backend/routes/comments.js`: API reads and writes comments using parameterized SQL.
- `database/schema.sql`: database and table definition.

## Root cause

The vulnerable page inserts untrusted comment data into an HTML parsing sink (`innerHTML`). The browser interprets attacker-controlled markup and event-handler attributes as active content.

## Implemented mitigation

Use safe DOM APIs and assign untrusted strings through `textContent`. This makes the value text rather than parsed HTML in this rendering context. Apply the same rule to every user-controlled value and avoid unsafe sinks elsewhere.

## Other mitigations to discuss

- **Context-aware output encoding:** encode data for its exact output context (HTML, attribute, URL, or JavaScript context).
- **Framework auto-escaping:** use framework defaults that render values as text; avoid raw-HTML escape hatches with untrusted data.
- **HTML sanitization:** if rich HTML is a real requirement, use a maintained allow-list sanitizer such as DOMPurify.
- **Content Security Policy (CSP):** restrict script sources and reduce the impact of injection; defense in depth, not a substitute for safe output handling.
- **HttpOnly cookies:** prevent JavaScript from reading cookies marked HttpOnly; this does not prevent XSS itself.
- **Safe DOM sinks:** prefer `textContent`, `createElement`, and safe property assignment over `innerHTML` for untrusted text.

## Safety note

This application intentionally contains a browser-side XSS vulnerability for a supervised lab. It binds only to `127.0.0.1`. Do not change it to listen on a public interface, deploy it, or test it against systems you do not own or have explicit permission to test.
