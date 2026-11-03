"""Request-level regression tests for the GET-based CSRF lab."""
import re
import unittest

from app import INITIAL_EMAIL, create_app
from attacker import app as attacker_app

PAYLOAD = "/change-email?email=attacker%40example.test"


class CSRFLabTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test-only"})
        self.client = self.app.test_client()
        self.client.post("/login")
        page = self.client.get("/").get_data(as_text=True)
        self.token = re.search(r'name="csrf_token" value="([^"]+)"', page)[1]

    def secure(self):
        return self.client.post("/configure", data={"mode": "secure", "csrf_token": self.token})

    def test_forged_get_changes_email_in_vulnerable_mode(self):
        response = self.client.get(PAYLOAD, headers={"Referer": "http://localhost:8001/"}, follow_redirects=True)
        self.assertIn(b'id="current-email">attacker@example.test', response.data)

    def test_identical_forged_get_blocked_after_fix(self):
        self.client.get(PAYLOAD)
        self.secure()
        response = self.client.get(PAYLOAD, headers={"Referer": "http://localhost:8001/"})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.headers["Allow"], "POST")
        self.assertIn(INITIAL_EMAIL.encode(), self.client.get("/").data)

    def test_secure_post_missing_or_wrong_token_blocked(self):
        self.secure()
        for token in (None, "forged-token"):
            data = {"email": "attacker@example.test"}
            if token:
                data["csrf_token"] = token
            self.assertEqual(self.client.post("/change-email", data=data).status_code, 403)
        self.assertIn(INITIAL_EMAIL.encode(), self.client.get("/").data)

    def test_secure_legitimate_post_succeeds(self):
        self.secure()
        response = self.client.post("/change-email", data={"email": "saqlain.updated@example.test", "csrf_token": self.token}, follow_redirects=True)
        self.assertIn(b'id="current-email">saqlain.updated@example.test', response.data)

    def test_another_sessions_token_is_rejected(self):
        self.secure()
        other = self.app.test_client()
        other.post("/login")
        page = other.get("/").get_data(as_text=True)
        other_token = re.search(r'name="csrf_token" value="([^"]+)"', page)[1]
        self.assertEqual(self.client.post("/change-email", data={"email": "attacker@example.test", "csrf_token": other_token}).status_code, 403)

    def test_unauthenticated_requests_do_not_mutate(self):
        self.assertEqual(self.app.test_client().get(PAYLOAD).status_code, 401)

    def test_head_is_read_only_in_both_modes(self):
        for mode in ("vulnerable", "secure"):
            self.client.post("/configure", data={"mode": mode, "csrf_token": self.token})
            self.assertEqual(self.client.head(PAYLOAD).status_code, 405)
            self.assertIn(INITIAL_EMAIL.encode(), self.client.get("/").data)

    def test_controls_require_token_and_reset_state(self):
        self.client.get(PAYLOAD)
        self.assertEqual(self.client.post("/configure", data={"mode": "secure"}).status_code, 403)
        self.secure()
        self.assertIn(INITIAL_EMAIL.encode(), self.client.get("/").data)

    def test_attack_page_contains_exact_payload(self):
        response = attacker_app.test_client().get("/")
        self.assertIn(('href="http://127.0.0.1:5000' + PAYLOAD + '"').encode(), response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
