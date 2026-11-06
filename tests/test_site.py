from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.scripts = []
        self.forms = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values)
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"])
        if tag == "form":
            self.forms.append(values)
        if tag in {"h1", "h2", "h3"}:
            self.headings.append(tag)


def parse(name):
    parser = PageParser()
    parser.feed((ROOT / name).read_text(encoding="utf-8"))
    return parser


class SiteContractTests(unittest.TestCase):
    def test_main_page_has_required_sections(self):
        page = parse("index.html")
        self.assertTrue(
            {"inicio", "filosofia", "diario", "recursos", "nosotras", "contacto"}
            <= page.ids
        )

    def test_main_page_has_single_h1_and_site_script(self):
        page = parse("index.html")
        self.assertEqual(page.headings.count("h1"), 1)
        self.assertIn("scripts/site.js", page.scripts)

    def test_amazon_and_legal_links_exist(self):
        page = parse("index.html")
        hrefs = {link.get("href") for link in page.links}
        self.assertIn("https://www.amazon.es/dp/B0HQ4X8MDZ", hrefs)
        self.assertTrue(
            {"aviso-legal.html", "privacidad.html", "cookies.html"} <= hrefs
        )

    def test_meditations_are_not_exposed(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8").lower()
        self.assertNotIn("<audio", source)
        self.assertNotIn('id="meditaciones"', source)
        self.assertNotIn(".mp3", source)

    def test_pending_forms_do_not_submit_data(self):
        page = parse("index.html")
        self.assertGreaterEqual(len(page.forms), 1)
        for form in page.forms:
            self.assertNotIn("action", form)

    def test_interactive_hooks_match_site_script_contract(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(source.count("data-dialog-close"), 2)
        self.assertNotIn("data-resource-close", source)
        self.assertIn("data-form-status", source)

    def test_site_script_uses_only_hooks_present_in_the_page(self):
        script = (ROOT / "scripts" / "site.js").read_text(encoding="utf-8")
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        for hook in (
            "data-menu-toggle",
            "data-navigation",
            "data-resource-open",
            "data-resource-dialog",
            "data-dialog-close",
            "data-brevo-pending",
            "data-form-status",
        ):
            self.assertIn(hook, script)
            self.assertIn(hook, page)

    def test_site_script_never_sends_data(self):
        script = (ROOT / "scripts" / "site.js").read_text(encoding="utf-8")
        for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "api-key"):
            self.assertNotIn(forbidden, script)

    def test_legal_pages_exist_and_are_marked_as_drafts(self):
        for name in ("aviso-legal.html", "privacidad.html", "cookies.html"):
            source = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("Borrador", source)
            self.assertIn('href="index.html', source)


if __name__ == "__main__":
    unittest.main()
