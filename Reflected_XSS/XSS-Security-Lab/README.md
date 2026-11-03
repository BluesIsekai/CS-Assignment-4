# XSS Security Lab: Reflected Cross-Site Scripting (Variant 2)

![Project Category](https://img.shields.io/badge/Category-Cybersecurity%20Education-blue)
![Vulnerability](https://img.shields.io/badge/CWE--79-Improper%20Neutralization%20of%20Input-red)
![Defense](https://img.shields.io/badge/Mitigation-Context--Aware%20Output%20Encoding-emerald)
![Framework](https://img.shields.io/badge/Backend-Python%20Flask%20%2B%20Jinja2-purple)
![Environment](https://img.shields.io/badge/Host-127.0.0.1%20Local-green)

A professional, cybersecurity-themed educational laboratory web application built for college computer science students and practical cybersecurity assignments.

This project specifically demonstrates **Reflected Cross-Site Scripting (XSS), Variant 2 (User Input Reflected in HTML Body Context)** and proves how **Context-Aware Output Encoding** through Jinja2 auto-escaping completely neutralizes client-side code injection.

---

## 🎯 Project Overview & Academic Purpose

Cross-Site Scripting (XSS) is categorized under **CWE-79** and **OWASP Top 10: A03:2021 – Injection**.

### What is Reflected XSS?
In Reflected XSS (Type 1 / Non-Persistent), malicious script data is sent as part of an HTTP request (such as a search query parameter) and reflected immediately back into the HTTP response. The exploit is **not stored in a database**; instead, an attacker tricks a victim into clicking a crafted hyperlink.

### What is Variant 2 (HTML Body Context)?
In **Variant 2**, the reflected data lands directly between HTML body tags:
```html
<div class="search-results">
    You searched for: [USER_INPUT]
</div>
```
Because the input is reflected directly inside HTML element content, an attacker does not need quotes to escape attributes—any tag metacharacters (`<`, `>`) immediately cause the browser's HTML tokenizer to transition to the **Tag Open State** and **Script Data State**.

---

## 🗂️ Project Directory Structure

The application consists strictly of the **four main sections** (Home, Vulnerable Lab, Secure Lab, and Comparison):

```text
XSS-Security-Lab/
│
├── app.py                      # Flask backend handling routes, GET queries, and localhost binding
├── requirements.txt            # Python dependencies (Flask, Jinja2, MarkupSafe, Werkzeug)
├── README.md                   # Complete documentation
│
├── templates/                  # Jinja2 HTML Templates (4 Core Views)
│   ├── base.html               # Master layout, cyber navbar (4 links only), and footer
│   ├── index.html              # 1. Home page with theory overview & lab launch cards
│   ├── vulnerable.html         # 2. Vulnerable search lab (renders {{ query | safe }})
│   ├── secure.html             # 3. Secure search lab (renders safe auto-escaped {{ query }})
│   └── comparison.html         # 4. Comparison (Code diff, root cause, & 6 mitigation alternatives)
│
├── static/                     # Frontend Assets
│   ├── css/
│   │   └── style.css           # Modern cyber dark navy theme, neon accents & layout
│   └── js/
│       └── script.js           # Interactive live encoder & 1-click payload tester
│
├── tests/                      # Automated Verification Test Suite
│   └── test_app.py             # Unit tests verifying exploit execution & escaping defense
│
└── screenshots/                # Laboratory verification screenshots
    ├── 01_home_page.png
    ├── 02_vulnerable_search_result.png
    ├── 03_secure_search_result.png
    ├── 04_code_comparison.png
    └── README.md
```

---

## 💻 Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.11+ / Flask 3.x | Lightweight HTTP routing, GET request parsing |
| **Templating** | Jinja2 + MarkupSafe | Demonstrates `\| safe` bypass vs default auto-escaping |
| **Frontend** | Semantic HTML5 | Clean, accessible DOM layout |
| **Styling** | Vanilla CSS3 | Dark navy cybersecurity theme with glassmorphism & gradients |
| **Scripting** | Vanilla JavaScript | Interactive live entity sandbox & mobile menu |
| **Testing** | Python `unittest` | Automated validation of exploit behavior and defenses |

---

## 🚀 Quickstart: Installation & Running Locally

### Step 1: Open Terminal in the Project Directory
```powershell
cd c:\Users\HP\Desktop\xss_security\XSS-Security-Lab
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Launch the Application
```powershell
python app.py
```

### Step 4: Open in Web Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

> **Note:** The application is also runnable directly from the root repository directory via `python app.py`.

---

## 🔬 Hands-On Lab Walkthrough

### 1. Home Page (`/`)
- Modern cybersecurity dark theme with glow badges and architecture metrics.
- Provides two prominent launch cards: **Vulnerable Search Lab** and **Secure Search Lab**.
- Explains what Reflected XSS is and illustrates the 4-phase attack lifecycle.

### 2. Vulnerable Search Lab (`/vulnerable`)
- Submits search query `q` via GET request.
- In `vulnerable.html`, query is rendered using `{{ query | safe }}`.
- Click the preset `[⚡ <script>alert(...)>]` button or submit:
  ```html
  <script>alert('Reflected XSS Detected in Vulnerable Lab!')</script>
  ```
- **Result:** The browser executes the JavaScript and displays the alert popup.
- Includes a Technical Inspector showing the unescaped response sink.

### 3. Secure Search Lab (`/secure`)
- Submits the exact same search query `q` via GET request.
- In `secure.html`, query is rendered using default Jinja2 auto-escaping `{{ query }}`.
- Submit the identical payload:
  ```html
  <script>alert('Reflected XSS Detected in Vulnerable Lab!')</script>
  ```
- **Result:** **No alert popup executes.** The text is displayed safely on screen as plain text.
- Includes a Technical Inspector showing how `<` and `>` were converted to `&lt;` and `&gt;`.

### 4. Code Comparison & Mitigation (`/comparison`)
- **Vulnerable vs Secure Source Code:** Side-by-side backend routes and template snippets.
- **Root Cause Analysis:** Explains how the failure to separate code from untrusted data leads to injection.
- **Implemented Mitigation:** Demonstrates HTML entity encoding with reference table and a live interactive encoding sandbox.
- **Other Mitigation Alternatives (Short Theory Section):**
  1. **Context-Aware Output Encoding:** Tailoring encoding to body, attribute, JS, CSS, or URL contexts.
  2. **Framework Auto-Escaping:** Automated escaping built into Jinja2, React, Angular, Vue.
  3. **HTML Sanitisation:** Safe allow-list parsing (DOMPurify, Bleach) when rich text is necessary.
  4. **Content Security Policy (CSP):** HTTP response headers (`default-src 'self'`) blocking inline scripts.
  5. **HttpOnly Cookies:** Protecting session identifiers from theft via `document.cookie`.
  6. **Safe DOM Sinks:** Preferring `textContent` over dangerous sinks like `innerHTML`.
- **Security Comparison Matrix:** Detailed feature-by-feature evaluation table.

---

## 🔤 HTML Entity Output Encoding Table

| Raw Character | Encoded Entity | Numeric Code | Defensive Purpose |
| :---: | :---: | :---: | :--- |
| `<` | `&lt;` | `&#60;` | Prevents opening any HTML tag or script boundary |
| `>` | `&gt;` | `&#62;` | Prevents closing an open tag or attribute early |
| `&` | `&amp;` | `&#38;` | Prevents entity confusion and double-decoding bypasses |
| `"` | `&quot;` | `&#34;` | Prevents breakout from double-quoted attributes |
| `'` | `&#39;` / `&amp;#x27;` | `&#39;` | Prevents breakout from single-quoted attributes |

---

## 🧪 Automated Testing

Run the automated test suite verifying all four sections and mitigation behaviors:
```powershell
python -m unittest discover -s tests -p "test_*.py"
```
Output:
```text
Ran 8 tests in 0.091s
OK
```

---

## 🔒 Security Restrictions
- Strictly bound to `127.0.0.1` (localhost).
- Testing is restricted to benign `alert()` popups.
- No external requests, destructive payloads, or credential theft vectors are utilized.
