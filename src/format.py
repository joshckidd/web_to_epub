import os
import mimetypes
from ebooklib import epub
# Use this for doc reference: https://pypi.org/project/EbookLib/

class WebBook:

    def __init__(self, ebook_values):
        self.image_folder = None
        self.book = epub.EpubBook()
        self.book.spine = ["nav"]

        if "id" in ebook_values:
            self.book.set_identifier(ebook_values["id"][0])
        if "title" in ebook_values:
            self.book.set_title(ebook_values["title"][0])
        if "language" in ebook_values:
            self.book.set_language(ebook_values["language"][0])
            self.default_language = ebook_values["language"][0]
        if "image-folder" in ebook_values:
            self.image_folder = 'output/'
            if ebook_values["image-folder"][0] != None:
                self.image_folder += ebook_values["image-folder"][0]
            
        for author in ebook_values["authors"]:
            self.book.add_author(author)

    def create_chapters(self, values_list):
        for values in values_list:
            c1 = epub.EpubHtml(title=values["title"][0], file_name=values["title"][0] + ".xhtml", lang=self.default_language)
            c1.content = (
                "<h1>" + values["title"][0] + "</h1>" + "<h2>by " + values["authors"][0] + "</h2>" + values["content"][0]
            )
            self.book.add_item(c1)
            self.book.spine.append(c1)
        if self.image_folder != None:
            images = os.listdir(self.image_folder)
            for image in images:
                mime_type, encoding = mimetypes.guess_type(self.image_folder + image)
                image_content = open(self.image_folder + image, "rb").read()
                img = epub.EpubImage(
                    uid="image_" + image,
                    file_name="static/" + image,
                    media_type=mime_type,
                    content=image_content,
                )
                self.book.add_item(img)

    def write_book(self):
        # define Table Of Contents
        self.book.toc = (
            epub.Link("chap_01.xhtml", "Introduction", "intro"),
            #(epub.Section("Simple book"), (c1,)),
        )

        # add default NCX and Nav file
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # define CSS style
        style = "BODY {color: white;}"
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style,
        )

        # add CSS file
        self.book.add_item(nav_css)

        # write to the file
        epub.write_epub("output/test.epub", self.book, {})
