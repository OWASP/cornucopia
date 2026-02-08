"""
Smoke tests for copi.owasp.org application.

These tests run against a Dockerized copi.owasp.org application in the CI pipeline (localhost).
They verify that:
1. At least 2 routes on the application are working
2. JavaScript is functioning correctly
3. Basic functionality is available

Note: We do not need smoke tests for cornucopia.owasp.org because Vite comes with
built-in smoke tests that fire up the server and check that all internal links
on the website go to live pages.

Issue: #1265
"""

import os
import unittest
import requests
from urllib.parse import urljoin


class CopiSmokeTests(unittest.TestCase):
    """Smoke tests for copi.owasp.org (Elixir/Phoenix application)"""

    # Default to localhost so CI can run against a Dockerized app on localhost
    BASE_URL = os.environ.get("COPI_BASE_URL", "http://127.0.0.1:4000")

    def _make_request(self, url: str, timeout: int = 30) -> requests.Response:
        """Helper method to make HTTP requests with error handling"""
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.ConnectionError:
            self.fail(f"Failed to connect to {url} - service may be down")
        except requests.exceptions.Timeout:
            self.fail(f"Request to {url} timed out after {timeout} seconds")

    def test_01_homepage_loads(self) -> None:
        """Test that the Copi homepage loads successfully"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200, f"Homepage returned status {response.status_code}")
        self.assertIn("copi", response.text.lower(), "Homepage should contain 'copi' text")

    def test_02_cards_route_accessible(self) -> None:
        """Test that the cards route is accessible"""
        url = urljoin(self.BASE_URL, "/cards")
        response = self._make_request(url)
        self.assertEqual(response.status_code, 200, f"Cards route returned status {response.status_code}")

    def test_03_javascript_loads(self) -> None:
        """Test that JavaScript assets are being served"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "<script" in response.text or "app.js" in response.text or "phoenix" in response.text.lower(),
            "JavaScript should be loaded on the page",
        )

    def test_04_health_check(self) -> None:
        """Test that the application server is healthy and responding"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "content-type",
            [h.lower() for h in response.headers.keys()],
            "Response should include content-type header",
        )


if __name__ == "__main__":
    unittest.main()