from src.settings import get_settings
from src.parse import get_values, get_links
from ebooklib import epub
# Use this for doc reference: https://pypi.org/project/EbookLib/

# image download test

def main():
    settings_dict = get_settings()
    links = get_links(settings_dict["sources"])
    url = links[0]
    values = get_values(url, settings_dict["values"])
    print(values["category"])
    print(values["author"])
    print(values["content"])
    print(values["title"])

    # pasted from ebooklib documentation
    # next step: Write a function to create the ebook and set the metadata based on settings in 
    # the yaml file. I also want to create "aggregate values" at the ebook and chapter level. So
    # I'll also want to collect the values for each chapter in a list for making ebook level
    # aggregate values. And I'll want to update all values to be either: static, find, or 
    # aggregate.

    book = epub.EpubBook()

    # set metadata
    book.set_identifier("id123456")
    book.set_title("Sample book")
    book.set_language("en")

    book.add_author("Author Authorowski")
    book.add_author(
        "Danko Bananko",
        file_as="Gospodin Danko Bananko",
        role="ill",
        uid="coauthor",
    )

    # create chapter
    c1 = epub.EpubHtml(title=values["title"][0], file_name="chap_01.xhtml", lang="hr")
    c1.content = (
        "<h1>Intro heading</h1>"
        "<p>Zaba je skocila u baru.</p>"
        '<p><img alt="[ebook logo]" src="static/ebooklib.gif"/><br/></p>'
    )

    # create image from the local image
    image_content = open("output/orphanplanetcover.jpg", "rb").read()
    img = epub.EpubImage(
        uid="image_1",
        file_name="static/ebooklib.gif",
        media_type="image/gif",
        content=image_content,
    )

    # add chapter
    book.add_item(c1)
    # add image
    book.add_item(img)

    # define Table Of Contents
    book.toc = (
        epub.Link("chap_01.xhtml", "Introduction", "intro"),
        (epub.Section("Simple book"), (c1,)),
    )

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    book.spine = ["nav", c1]

    # write to the file
    epub.write_epub("output/test.epub", book, {})

if __name__ == "__main__":
    main()
