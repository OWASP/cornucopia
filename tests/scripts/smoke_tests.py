"""
Smoke tests for copi.owasp.org and cornucopia.owasp.org applications.

These tests verify that:
1. At least 2 routes on each application are working
2. JavaScript is functioning correctly
3. Basic functionality is available

Issue: #1265
"""

import os
import unittest
import requests
import time
from urllib.parse import urljoin


class CopiSmokeTests(unittest.TestCase):
    """Smoke tests for copi.owasp.org (Elixir/Phoenix application)"""

    BASE_URL = os.environ.get("COPI_BASE_URL", "https://copi.owasp.org")

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
            '<script' in response.text or 'app.js' in response.text or 'phoenix' in response.text.lower(),
            "JavaScript should be loaded on the page"
        )

    def test_04_health_check(self) -> None:
        """Test that the application server is healthy and responding"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('content-type', [h.lower() for h in response.headers.keys()],
                     "Response should include content-type header")


class CornucopiaSmokeTests(unittest.TestCase):
    """Smoke tests for cornucopia.owasp.org (SvelteKit application)"""

    BASE_URL = os.environ.get("CORNUCOPIA_BASE_URL", "https://cornucopia.owasp.org")

    def _make_request(self, url: str, timeout: int = 30) -> requests.Response:
        """Helper method to make HTTP requests with error handling"""
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.ConnectionError:
            self.fail(f"Failed to connect to {url} - service may be down")
        except requests.exceptions.Timeout:
            self.fail(f"Request to {url} timed out after {timeout} seconds")

    def test_01_homepage_loads(self) -> None:
        """Test that the Cornucopia homepage loads successfully"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200, f"Homepage returned status {response.status_code}")
        self.assertIn("cornucopia", response.text.lower(), "Homepage should contain 'cornucopia' text")

    def test_02_cards_route_accessible(self) -> None:
        """Test that the cards browser route is accessible"""
        url = urljoin(self.BASE_URL, "/cards")
        response = self._make_request(url)
        self.assertEqual(response.status_code, 200, f"Cards route returned status {response.status_code}")

    def test_03_javascript_loads(self) -> None:
        """Test that JavaScript/Svelte bundles are being served"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '<script' in response.text or '_app' in response.text or 'svelte' in response.text.lower(),
            "JavaScript/Svelte should be loaded on the page"
        )

    def test_04_card_detail_route_accessible(self) -> None:
        """Test that individual card routes are accessible"""
        url = urljoin(self.BASE_URL, "/cards/VE2")
        response = self._make_request(url)
        self.assertEqual(response.status_code, 200, f"Card detail route returned status {response.status_code}")

    def test_05_javascript_execution_check(self) -> None:
        """Test that the page structure indicates JavaScript is functional"""
        response = self._make_request(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        content = response.text
        sveltekit_markers = (
            "data-sveltekit-preload-data",
            "data-sveltekit-hydrate",
            "__sveltekit",
        )
        has_sveltekit_markers = any(marker in content for marker in sveltekit_markers)
        has_module_script = '<script type="module"' in content
        has_app_structure = has_sveltekit_markers or has_module_script
        self.assertTrue(has_app_structure, "Page should have structure for JavaScript execution")


class IntegrationSmokeTests(unittest.TestCase):
    """Integration tests checking both applications together"""

    COPI_URL = os.environ.get("COPI_BASE_URL", "https://copi.owasp.org")
    CORNUCOPIA_URL = os.environ.get("CORNUCOPIA_BASE_URL", "https://cornucopia.owasp.org")

    def _make_request(self, url: str, timeout: int = 30) -> requests.Response:
        """Helper method to make HTTP requests with error handling"""
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.ConnectionError as e:
            self.fail(f"Failed to connect to {url} - {str(e)}")
        except requests.exceptions.Timeout:
            self.fail(f"Request to {url} timed out after {timeout} seconds")

    def test_both_applications_responsive(self) -> None:
        """Test that both applications respond within acceptable time"""
        start_time = time.time()
        copi_response = self._make_request(self.COPI_URL)
        copi_time = time.time() - start_time

        start_time = time.time()
        cornucopia_response = self._make_request(self.CORNUCOPIA_URL)
        cornucopia_time = time.time() - start_time

        self.assertEqual(copi_response.status_code, 200, "Copi should be accessible")
        self.assertEqual(cornucopia_response.status_code, 200, "Cornucopia should be accessible")

        self.assertLess(copi_time, 30, f"Copi took {copi_time:.2f}s to respond")
        self.assertLess(cornucopia_time, 30, f"Cornucopia took {cornucopia_time:.2f}s to respond")


if __name__ == "__main__":
    unittest.main()
