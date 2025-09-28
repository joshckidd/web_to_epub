import os
from src.settings import get_settings, TEMPLATE_DIR
from src.web_book import WebBook

# tasks to finish:
# add toc 
# add sections 
# add pages 
# add cover
# css function
# add documentation

def main():
    template_files = os.listdir(TEMPLATE_DIR)
    for file in template_files:
        if file[-4:] == ".yml":
            settings_dict = get_settings(file)
            book = WebBook(settings_dict)
            book.write_book()

if __name__ == "__main__":
    main()
