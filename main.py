import os
from src.settings import get_settings, TEMPLATE_DIR
from src.web_book import WebBook

# tasks to finish:
# add cover
# tests for toc and template values
# tests for css
# tests for sections
# tests for pages
# tests for cover
# add documentation

def main():
    template_files = os.listdir(TEMPLATE_DIR)
    for file in template_files:
        if file[-4:] == ".yml":
            book = WebBook(get_settings(file))
            book.write_book()

if __name__ == "__main__":
    main()
