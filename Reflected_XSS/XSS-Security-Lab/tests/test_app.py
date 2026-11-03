"""
=============================================================================
XSS SECURITY LAB - AUTOMATED TEST SUITE
=============================================================================
Verifies:
1. All application endpoints return HTTP 200 OK.
2. The vulnerable endpoint reflects unescaped script payloads into the DOM.
3. The secure endpoint neutralizes identical payloads via HTML entity encoding.
4. Payload analysis API works properly.
=============================================================================
"""

import sys
from pathlib import Path
import unittest

# Ensure parent directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import app


class XSSSecurityLabTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page_loads(self):
        """Verify the Home Page renders with expected cybersecurity lab elements."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn("Reflected Cross-Site Scripting", data)
        self.assertIn("Vulnerable Search Lab", data)
        self.assertIn("Secure Search Lab", data)

    def test_vulnerable_page_initial_load(self):
        """Verify the Vulnerable Lab page loads with warning banner."""
        response = self.client.get('/vulnerable')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn("Intentionally Vulnerable Educational Environment", data)
        self.assertIn("UNPROTECTED SINK", data)

    def test_vulnerable_endpoint_demonstrates_reflected_xss(self):
        """
        CRITICAL VULNERABILITY TEST:
        Submitting an unescaped <script> payload must be reflected directly
        into the HTML body stream without entity escaping.
        """
        payload = "<script>alert('Reflected-XSS-Variant-2-Test')</script>"
        response = self.client.get(f'/vulnerable?q={payload}')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        
        # Verify the RAW unescaped script tag is present in the response
        self.assertIn(payload, data)
        self.assertIn("Unsanitized Response Sink", data)

    def test_secure_page_initial_load(self):
        """Verify the Secure Lab page loads with defensive security banner."""
        response = self.client.get('/secure')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn("Context-Aware Output Encoding Active", data)
        self.assertIn("AUTO-ESCAPING ACTIVE", data)

    def test_secure_endpoint_neutralizes_xss_payload(self):
        """
        CRITICAL MITIGATION TEST:
        Submitting the identical <script> payload must NOT be reflected raw;
        it MUST be escaped into HTML entities (&lt;script&gt;).
        """
        payload = "<script>alert('Reflected-XSS-Variant-2-Test')</script>"
        response = self.client.get(f'/secure?q={payload}')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')

        # Verify that the unescaped script tag is NOT in the rendered output sink
        self.assertIn("&lt;script&gt;alert(&#39;Reflected-XSS-Variant-2-Test&#39;)&lt;/script&gt;", data)
        self.assertIn("Encoded via Jinja2 Auto-Escaping (Safe)", data)

    def test_code_comparison_page(self):
        """Verify the side-by-side code comparison page renders successfully with all mitigation alternatives."""
        response = self.client.get('/comparison')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn("Vulnerable vs Secure Code Implementation", data)
        self.assertIn("Root Cause Analysis", data)
        self.assertIn("Implemented Mitigation: Output Encoding", data)
        self.assertIn("Other Mitigation Alternatives", data)
        self.assertIn("Context-Aware Output Encoding", data)
        self.assertIn("Framework Auto-Escaping", data)
        self.assertIn("HTML Sanitisation", data)
        self.assertIn("Content Security Policy", data)
        self.assertIn("HttpOnly Cookies", data)
        self.assertIn("Safe DOM Sinks", data)
        self.assertIn("Security Comparison Matrix", data)

    def test_education_route_removed(self):
        """Verify that the separate education/viva route has been completely removed."""
        response = self.client.get('/education')
        self.assertEqual(response.status_code, 404)

    def test_api_analyze_payload(self):
        """Verify the JSON API analyzer accurately flags and encodes payloads."""
        payload = "<img src=x onerror=alert(1)>"
        response = self.client.post('/api/analyze', json={'payload': payload})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['is_potentially_harmful'])
        self.assertIn('<', json_data['dangerous_detected'])
        self.assertEqual(json_data['escaped'], "&lt;img src=x onerror=alert(1)&gt;")


if __name__ == '__main__':
    unittest.main()
