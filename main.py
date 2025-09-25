from src.settings import get_settings
from src.parse import get_values_list, get_links, get_ebook_values
from src.web_book import WebBook

# next steps: 
# make it so you only pass the settings to WebBook
# add toc
# check on image folder settings
# image download test
# static and aggregate test
# epub metadata test
# epub chapter tests


def main():
    settings_dict = get_settings()
    values_list = get_values_list(get_links(settings_dict["sources"]), settings_dict["values"])
    book = WebBook(get_ebook_values(values_list, settings_dict["ebook-values"]))
    book.create_chapters(values_list)
    book.write_book()

if __name__ == "__main__":
    main()
