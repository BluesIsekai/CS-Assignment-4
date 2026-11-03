"""
=============================================================================
PROJECT: XSS Security Lab
TOPIC: Reflected Cross-Site Scripting (XSS) - Variant 2 Demonstration & Defense
PURPOSE: Educational Cybersecurity Web Application for College Students & Viva
=============================================================================
DESCRIPTION:
This Flask application demonstrates the mechanics of Reflected Cross-Site
Scripting (XSS) and how context-aware output encoding (via Jinja2 autoescaping)
neutralizes malicious user payloads.

SECURITY RESTRICTION:
- Local educational lab bound strictly to 127.0.0.1.
- Harmless, alert-based proof of concept (PoC) testing only.
=============================================================================
"""

import html
import markupsafe
from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Application Configuration
app.config['SECRET_KEY'] = 'educational-xss-lab-secret-key-college-demo'


# ============================================================================
# ROUTE 1: HOME PAGE
# ============================================================================
@app.route('/')
def index():
    """
    Renders the Home Page.
    Provides an introduction to Reflected XSS, the purpose of this experiment,
    and navigation cards for the Vulnerable and Secure labs.
    """
    return render_template('index.html', active_page='home')


# ============================================================================
# ROUTE 2: VULNERABLE SEARCH LAB (Reflected XSS Variant 2)
# ============================================================================
@app.route('/vulnerable')
def vulnerable():
    """
    VULNERABLE ENDPOINT: Demonstrates Reflected Cross-Site Scripting.
    
    HOW IT WORKS:
    1. The user's search query 'q' is extracted from the GET request URL parameters.
    2. The input is passed directly to the Jinja2 template.
    3. IN THE TEMPLATE (vulnerable.html), the query is rendered using the `| safe`
       filter: `{{ query | safe }}`.
    4. By marking the input as 'safe', Jinja2 bypasses automatic HTML entity escaping.
    5. The browser receives raw HTML/JavaScript characters (e.g. <script>, onerror, <img>)
       and the browser's HTML parser switches to execution mode, running the injected script!
       
    ROOT CAUSE:
    Mixing untrusted user input directly into the executable HTML document structure
    without context-aware sanitization or output encoding.
    """
    # Extract 'q' query parameter from GET request (default to empty string)
    query = request.args.get('q', '')
    
    # Calculate escaped version purely for educational comparison drawer
    escaped_preview = str(markupsafe.escape(query)) if query else ''
    
    return render_template(
        'vulnerable.html',
        query=query,
        escaped_preview=escaped_preview,
        has_searched=('q' in request.args),
        active_page='vulnerable'
    )


# ============================================================================
# ROUTE 3: SECURE SEARCH LAB (Output Encoding Enabled)
# ============================================================================
@app.route('/secure')
def secure():
    """
    SECURE ENDPOINT: Demonstrates Output Encoding Mitigation.
    
    HOW IT WORKS:
    1. The user's search query 'q' is extracted from the GET request URL parameters.
    2. The input is passed to the Jinja2 template as normal data.
    3. IN THE TEMPLATE (secure.html), the query is rendered naturally: `{{ query }}`.
    4. Jinja2's default auto-escaping engine translates sensitive HTML characters into
       safe HTML character entities:
          <  --> &lt;
          >  --> &gt;
          &  --> &amp;
          "  --> &quot;
          '  --> &#x27;
    5. When the browser receives these entities, the HTML parser treats them as text nodes
       (TextNodes), NOT executable HTML elements. The script NEVER executes!
    """
    # Extract 'q' query parameter from GET request
    query = request.args.get('q', '')
    
    # For educational transparency, show the exact escaped string generated
    escaped_preview = str(markupsafe.escape(query)) if query else ''
    
    return render_template(
        'secure.html',
        query=query,
        escaped_preview=escaped_preview,
        has_searched=('q' in request.args),
        active_page='secure'
    )


# ============================================================================
# ROUTE 4: CODE COMPARISON & MITIGATION
# ============================================================================
@app.route('/comparison')
def comparison():
    """
    Renders the side-by-side technical code comparison between the vulnerable
    and secure implementations, root cause analysis, output encoding mechanics,
    and other mitigation alternatives.
    """
    return render_template('comparison.html', active_page='comparison')


# ============================================================================
# HELPER API: INTERACTIVE PAYLOAD ANALYZER (Client-side interactive tool)
# ============================================================================
@app.route('/api/analyze', methods=['POST'])
def analyze_payload():
    """
    Educational JSON API helper:
    Receives a string payload and returns a tokenized breakdown of how
    output encoding neutralizes each dangerous character.
    """
    data = request.get_json(silent=True) or {}
    payload = data.get('payload', '')
    
    dangerous_chars = ['<', '>', '"', "'", '&', '`', '/']
    found_chars = [ch for ch in dangerous_chars if ch in payload]
    
    escaped = html.escape(payload)
    
    return jsonify({
        'original': payload,
        'escaped': escaped,
        'dangerous_detected': found_chars,
        'is_potentially_harmful': len(found_chars) > 0,
        'characters_count': len(payload),
        'escaped_length': len(escaped)
    })


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    print("=" * 70)
    print(" XSS SECURITY LAB - Educational Cyber Lab")
    print(" Topic: Reflected Cross-Site Scripting (XSS) Variant 2")
    print(" Local address: http://127.0.0.1:5000")
    print(" Press CTRL+C to terminate.")
    print("=" * 70)
    # Strictly bind to localhost (127.0.0.1) for secure educational isolation
    app.run(host='127.0.0.1', port=5000, debug=True)
