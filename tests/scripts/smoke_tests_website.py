"""
Smoke tests for cornucopia.owasp.org website.

Dynamically derives all translation routes from:
- cornucopia.owasp.org/application.yaml (editions, versions, draft languages)
- source/ directory (available language files)

Tests that at least one card route per edition/version/language
returns 200 (no 404 or 500).

Issue: #3663
"""

import os
import re
import unittest
import requests
import yaml
from pathlib import Path

BASE_URL = os.environ.get("CORNUCOPIA_BASE_URL", "https://cornucopia.owasp.org")

REPO_ROOT = Path(__file__).resolve().parents[2]
application.yaml = REPO_ROOT / "cornucopia.owasp.org" / "application.yaml"
SOURCE_DIR = REPO_ROOT / "source"


def get_decks():
    with open(application.yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["decks"]


def get_available_languages(edition: str, version: str, draft_languages: list) -> list:
    """
    Scans source/ for files matching {edition}-cards-{version}-{lang}.yaml
    and returns languages not in draft_languages.
    """
    pattern = re.compile(rf"^{re.escape(edition)}-cards-{re.escape(version)}-([a-z]{{2}}(?:_[a-z]{{2}})?)\\.yaml$")
    langs = []
    for f in SOURCE_DIR.iterdir():
        match = pattern.match(f.name)
        if match:
            lang = match.group(1)
            if lang not in draft_languages:
                langs.append(lang)
    return langs


def build_test_routes():
    """
    Builds a list of (edition, version, lang, url) tuples for all
    non-draft, non-external edition/version/language combinations.
    """
    decks = get_decks()
    routes = []

    for deck in decks:
        if deck.get("external"):
            continue

        edition = deck["edition"]
        card = deck["defaultPreviewCard"]

        for version_entry in deck["versions"]:
            version = version_entry["version"]
            draft_langs = version_entry.get("draftLanguages", [])
            langs = get_available_languages(edition, version, draft_langs)

            for lang in langs:
                # webapp 2.2 English has no lang suffix
                if edition == "webapp" and version == "2.2" and lang == "en":
                    path = f"/edition/{edition}/{card}/{version}"
                else:
                    path = f"/edition/{edition}/{card}/{version}/{lang}"

                routes.append((edition, version, lang, f"{BASE_URL}{path}"))

    return routes


def build_api_routes():
    """
    Builds /api/lang/{edition}/{version} routes for all
    non-external editions.
    """
    decks = get_decks()
    routes = []

    for deck in decks:
        if deck.get("external"):
            continue
        for version_entry in deck["versions"]:
            version = version_entry["version"]
            url = f"{BASE_URL}/api/lang/{deck['edition']}/{version}"
            routes.append((deck["edition"], version, url))

    return routes


class CornucopiaWebsiteSmokeTests(unittest.TestCase):
    """Smoke tests for cornucopia.owasp.org translation routes"""

    def _get(self, url: str) -> requests.Response:
        try:
            return requests.get(url, timeout=30)
        except requests.exceptions.ConnectionError:
            self.fail(f"Failed to connect to {url}")
        except requests.exceptions.Timeout:
            self.fail(f"Request timed out: {url}")

    def test_edition_translation_routes(self):
        """
        Test that all non-draft edition/version/language routes
        return 200 and not 404 or 500.
        """
        routes = build_test_routes()
        self.assertGreater(len(routes), 0, "No routes found — check application.yaml and source/")

        failures = []
        for edition, version, lang, url in routes:
            resp = self._get(url)
            if resp.status_code in (404, 500):
                failures.append(f"{resp.status_code} {url}")

        if failures:
            self.fail(f"{len(failures)} route(s) failed:\n" + "\n".join(failures))

    def test_api_lang_routes(self):
        """
        Test that all /api/lang/{edition}/{version} routes
        return 200 and not 404 or 500.
        """
        routes = build_api_routes()
        self.assertGreater(len(routes), 0, "No API routes found")

        failures = []
        for edition, version, url in routes:
            resp = self._get(url)
            if resp.status_code in (404, 500):
                failures.append(f"{resp.status_code} {url}")

        if failures:
            self.fail(f"{len(failures)} API route(s) failed:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
