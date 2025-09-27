import unittest
import src.settings
import src.web_book

class TestWebBook(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWebBook, self).__init__(*args, **kwargs)
        settings_dict = src.settings.get_settings("template_test.yml")
        self.book = src.web_book.WebBook(settings_dict)

    def test_get_links(self):
        links = self.book.links
        self.assertEqual(links[0], "https://joshckidd.github.io/static_site/blog/glorfindel", "The first link is wrong.")

    def test_get_values(self):
        values = self.book.values_list[0]
        self.assertEqual(values["title"][0], "Why Glorfindel is More Impressive than Legolas", "The first title is wrong.")
