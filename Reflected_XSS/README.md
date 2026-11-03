# XSS Security Lab: Reflected Cross-Site Scripting (Variant 2)

![Project Category](https://img.shields.io/badge/Category-Cybersecurity%20Education-blue)
![Vulnerability](https://img.shields.io/badge/CWE--79-Improper%20Neutralization%20of%20Input-red)
![Defense](https://img.shields.io/badge/Mitigation-Context--Aware%20Output%20Encoding-emerald)
![Framework](https://img.shields.io/badge/Backend-Python%20Flask%20%2B%20Jinja2-purple)
![Environment](https://img.shields.io/badge/Host-127.0.0.1%20Local-green)

A professional, cybersecurity-themed educational laboratory web application built for college cybersecurity assignments.

This project demonstrates **Reflected Cross-Site Scripting (XSS), Variant 2 (User Input Reflected in HTML Body Context)** and proves how **Context-Aware Output Encoding** through Jinja2 auto-escaping completely neutralizes client-side code injection.

---

## 🗂️ Project Directory Structure

The complete project is located in `XSS-Security-Lab/` with **only four core sections**:

```text
XSS-Security-Lab/
│
├── app.py                      # Core Python Flask backend with vulnerable & secure routes
├── requirements.txt            # Python dependencies (Flask, Jinja2, MarkupSafe, Werkzeug)
├── README.md                   # Complete academic documentation
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

## 🚀 Quickstart: Running the Lab

### From the Root Directory:
```powershell
python app.py
```

### Or From inside `XSS-Security-Lab`:
```powershell
cd XSS-Security-Lab
python app.py
```

### Access in Browser:
```text
http://127.0.0.1:5000
```

### Run Automated Tests:
```powershell
python -m unittest discover -s XSS-Security-Lab/tests -p "test_*.py"
```

For full details, see [XSS-Security-Lab/README.md](XSS-Security-Lab/README.md).
