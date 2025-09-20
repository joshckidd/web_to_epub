import unittest
import src.settings

class TestSettings(unittest.TestCase):

    def test_get_settings(self):
        settings_dict = src.settings.get_settings(testing=True)
        self.assertEqual(settings_dict["sources"]["link-pages"][0]["url"], "https://joshckidd.github.io/static_site/", "The first link page url is wrong.")
        self.assertEqual(settings_dict["values"]["title"]["find"], "h1 text", "The search string for title is wrong.")