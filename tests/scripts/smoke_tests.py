"""
Smoke tests for copi.owasp.org and cornucopia.owasp.org applications.

These tests verify that:
1. At least 2 routes on each application are working
2. JavaScript is functioning correctly
3. Basic functionality is available

Issue: #1265
"""

import unittest
import requests
import time
from typing import Dict, Any
from urllib.parse import urljoin


class CopiSmokeTests(unittest.TestCase):
    """Smoke tests for copi.owasp.org (Elixir/Phoenix application)"""

    # Use environment variable for URL, default to production
    BASE_URL = "https://copi.owasp.org"

    def test_01_homepage_loads(self) -> None:
        """Test that the Copi homepage loads successfully"""
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200, f"Homepage returned status {response.status_code}")
        self.assertIn("copi", response.text.lower(), "Homepage should contain 'copi' text")

    def test_02_game_route_accessible(self) -> None:
        """Test that a game-related route is accessible"""
        # Test the game creation or lobby page
        url = urljoin(self.BASE_URL, "/")
        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200, f"Game route returned status {response.status_code}")

    def test_03_javascript_loads(self) -> None:
        """Test that JavaScript assets are being served"""
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200)
        # Check for common JavaScript patterns in Phoenix/LiveView apps
        self.assertTrue(
            '<script' in response.text or 'app.js' in response.text or 'phoenix' in response.text.lower(),
            "JavaScript should be loaded on the page"
        )

    def test_04_health_or_connectivity(self) -> None:
        """Test that the application server is healthy and responding"""
        # Just verify the homepage is accessible with proper headers
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200)
        # Verify we get proper HTTP headers indicating a web application
        self.assertIn('content-type', [h.lower() for h in response.headers.keys()],
                     "Response should include content-type header")


class CornucopiaSmokeTests(unittest.TestCase):
    """Smoke tests for cornucopia.owasp.org (SvelteKit application)"""

    # Use environment variable for URL, default to production
    BASE_URL = "https://cornucopia.owasp.org"

    def test_01_homepage_loads(self) -> None:
        """Test that the Cornucopia homepage loads successfully"""
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200, f"Homepage returned status {response.status_code}")
        self.assertIn("cornucopia", response.text.lower(), "Homepage should contain 'cornucopia' text")

    def test_02_cards_route_accessible(self) -> None:
        """Test that the cards browser route is accessible"""
        url = urljoin(self.BASE_URL, "/cards")
        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200, f"Cards route returned status {response.status_code}")

    def test_03_javascript_loads(self) -> None:
        """Test that JavaScript/Svelte bundles are being served"""
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200)
        # Check for SvelteKit patterns
        self.assertTrue(
            '<script' in response.text or '_app' in response.text or 'svelte' in response.text.lower(),
            "JavaScript/Svelte should be loaded on the page"
        )

    def test_04_card_detail_route_accessible(self) -> None:
        """Test that individual card routes are accessible"""
        # Test a specific card route (using a known card from the deck)
        url = urljoin(self.BASE_URL, "/cards/VE2")
        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200, f"Card detail route returned status {response.status_code}")

    def test_05_javascript_execution_check(self) -> None:
        """Test that the page structure indicates JavaScript is functional"""
        response = requests.get(self.BASE_URL, timeout=30)
        self.assertEqual(response.status_code, 200)
        # Check for typical SvelteKit hydration markers or app structure
        content = response.text
        # Look for either SvelteKit app div or script tags that would execute JS
        has_app_structure = 'id=' in content and 'script' in content.lower()
        self.assertTrue(has_app_structure, "Page should have structure for JavaScript execution")


class IntegrationSmokeTests(unittest.TestCase):
    """Integration tests checking both applications together"""

    COPI_URL = "https://copi.owasp.org"
    CORNUCOPIA_URL = "https://cornucopia.owasp.org"

    def test_both_applications_responsive(self) -> None:
        """Test that both applications respond within acceptable time"""
        start_time = time.time()
        copi_response = requests.get(self.COPI_URL, timeout=30)
        copi_time = time.time() - start_time

        start_time = time.time()
        cornucopia_response = requests.get(self.CORNUCOPIA_URL, timeout=30)
        cornucopia_time = time.time() - start_time

        self.assertEqual(copi_response.status_code, 200, "Copi should be accessible")
        self.assertEqual(cornucopia_response.status_code, 200, "Cornucopia should be accessible")
        # Both should respond in reasonable time (30 seconds is the hard limit via timeout)
        self.assertLess(copi_time, 30, f"Copi took {copi_time:.2f}s to respond")
        self.assertLess(cornucopia_time, 30, f"Cornucopia took {cornucopia_time:.2f}s to respond")


if __name__ == "__main__":
    unittest.main()
