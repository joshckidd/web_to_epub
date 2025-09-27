from src.settings import get_settings
from src.web_book import WebBook

# next steps: 
# search for all merge fields in a template
# add toc 
# image test
# static and aggregate test
# epub metadata test
# epub chapter tests


def main():
    settings_dict = get_settings()
    book = WebBook(settings_dict)
    book.write_book()

if __name__ == "__main__":
    main()
