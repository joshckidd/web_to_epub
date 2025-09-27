import os
from src.settings import get_settings
from src.web_book import WebBook

# next steps:
# add toc 
# image test
# static and aggregate test
# epub metadata test
# epub chapter tests


def main():
    template_files = os.listdir("template/")
    for file in template_files:
        if file[-4:] == ".yml":
            settings_dict = get_settings(file)
            book = WebBook(settings_dict)
            book.write_book()

if __name__ == "__main__":
    main()
