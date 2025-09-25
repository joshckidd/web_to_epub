from src.settings import get_settings
from src.parse import get_values_list, get_links, get_ebook_values
from src.format import WebBook
from ebooklib import epub
# Use this for doc reference: https://pypi.org/project/EbookLib/

# image download test
# static and aggregate test
# epub metadata test

def main():
    settings_dict = get_settings()
    links = get_links(settings_dict["sources"])
    values_list = get_values_list(links, settings_dict["values"])

    # next step: add toc
    # check on image folder settings

    book = WebBook(get_ebook_values(values_list, settings_dict["ebook-values"]))
    book.create_chapters(values_list)
    book.write_book()

if __name__ == "__main__":
    main()
