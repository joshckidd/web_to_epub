import unittest
import src.settings

class TestSettings(unittest.TestCase):

    def test_get_settings(self):
        settings_dict = src.settings.get_settings(testing=True)
        self.assertEqual(settings_dict["sources"]["links"][0], "https://www.example.com/", "The first link is wrong.")
        self.assertEqual(settings_dict["values"]["title"]["find"], "div#title", "The search string for title is wrong.")