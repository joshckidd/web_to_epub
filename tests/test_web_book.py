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
        item = self.book.get_item_with_id("image_glorfindel.png")
        self.assertEqual(item.id, "image_glorfindel.png", "The first image id is wrong.")
        self.assertEqual(item.file_name, "static/glorfindel.png", "The first image file name is wrong.")

    def test_metadata(self):
        self.assertEqual(self.book.uid, "uri:https://joshckidd.github.io/static_site/", "The book uid is wrong.")
        self.assertEqual(self.book.title, "WebBook Test", "The book title is wrong.")

    def test_chapters(self):
        item = self.book.get_item_with_id("chapter_0")
        self.assertEqual(item.id, "chapter_0", "The first chapter id is wrong.")
        self.assertIn("<p>In J.R.R. Tolkien's legendarium", item.content, "The first chapter content is wrong.")
        self.assertNotIn("<code>", item.content, "The first chapter content is wrong.")

    def test_cover(self):
        item = self.book.get_item_with_id("cover")
        self.assertEqual(item.id, "cover", "The cover id is wrong.")
        self.assertEqual(item.file_name, "cover.xhtml", "The cover file name is wrong.")

    def test_toc(self):
        item = self.book.get_item_with_id("nav")
        self.assertEqual(item.id, "nav", "The toc id is wrong.")
        self.assertEqual(item.file_name, "nav.xhtml", "The toc file name is wrong.")
        item = self.book.toc[1][1][0]
        self.assertIn('Why Glorfindel is More Impressive than Legolas by Boots', item.title, "The first chapter name is wrong.")

    def test_css(self):
        item = self.book.get_item_with_id("css_css1")
        self.assertEqual(item.id, "css_css1", "The css id is wrong.")
        self.assertEqual(item.file_name, "styles.css", "The css file name is wrong.")
        self.assertIn('BODY {color: white;}', item.content, "The css content is wrong.")

    def test_page(self):
        item = self.book.get_item_with_id("title-page")
        self.assertEqual(item.id, "title-page", "The title page id is wrong.")
        self.assertEqual(item.file_name, "title-page.xhtml", "The title page file name is wrong.")
        self.assertIn('<h1>WebBook Test</h1>', item.content, "The title page content is wrong.")

    def test_section(self):
        item = self.book.get_item_with_id("blog-posts")
        self.assertEqual(item.id, "blog-posts", "The section page id is wrong.")
        self.assertEqual(item.file_name, "blog-posts.xhtml", "The section page file name is wrong.")
        self.assertIn('<h1>Blog Posts</h1>', item.content, "The section page content is wrong.")