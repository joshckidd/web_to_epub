import unittest
import src.settings
import src.parse

class TestParse(unittest.TestCase):

    def test_get_links(self):
        settings_dict = src.settings.get_settings(testing=True)
        links = src.parse.get_links(settings_dict["sources"])
        self.assertEqual(links[0], "https://joshckidd.github.io/static_site/blog/glorfindel", "The first link is wrong.")

    def test_get_values(self):
        settings_dict = src.settings.get_settings(testing=True)
        links = src.parse.get_links(settings_dict["sources"])
        values = src.parse.get_values(links[0], settings_dict["values"])
        self.assertEqual(values["title"][0], "Why Glorfindel is More Impressive than Legolas", "The first title is wrong.")
