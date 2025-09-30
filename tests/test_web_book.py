import unittest
import src.settings
import src.web_book

class TestWebBook(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWebBook, self).__init__(*args, **kwargs)
        settings_dict = src.settings.get_settings("template_test.yml")
        self.book = src.web_book.WebBook(settings_dict)

    def test_links(self):
        links = self.book.links
        self.assertEqual(links[0], "https://joshckidd.github.io/static_site/blog/glorfindel", "The first link is wrong.")

    def test_values(self):
        values = self.book.values_list[0]
        self.assertEqual(values["title"][0], "Why Glorfindel is More Impressive than Legolas", "The first title is wrong.")
        self.assertEqual(values["author"][0], "Boots", "The author value is wrong.")
        self.assertEqual(self.book.ebook_values["titles"][0], 'Why Glorfindel is More Impressive than Legolas and Why Tom Bombadil Was a Mistake and The Unparalleled Majesty of "The Lord of the Rings"', "The article titles are wrong.")

    def test_images(self):
        self.assertEqual(self.book.items[0].id, "image_glorfindel.png", "The first image id is wrong.")
        self.assertEqual(self.book.items[0].file_name, "static/glorfindel.png", "The first image file name is wrong.")

    def test_metadata(self):
        self.assertEqual(self.book.uid, "uri:https://joshckidd.github.io/static_site/", "The book uid is wrong.")
        self.assertEqual(self.book.title, "WebBook Test", "The book title is wrong.")

    def test_chapters(self):
        self.assertEqual(self.book.items[3].id, "chapter_0", "The first chapter id is wrong.")
        self.assertIn("<p>In J.R.R. Tolkien's legendarium", self.book.items[3].content, "The first chapter content is wrong.")
