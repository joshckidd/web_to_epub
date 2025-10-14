import os
from src.settings import get_settings, TEMPLATE_DIR
from src.web_book import WebBook
from src.cover import resize_and_crop_to_png, overlay_png, add_text_to_image

def main():
#    resize_and_crop_to_png("template/default-header-5.jpg", "output/cover.png", 1600, 2560)
#    overlay_png("output/cover.png", "template/SH_cover_logo.png", "output/cover.png")
#    overlay_png("output/cover.png", "template/samovar_logo.png", "output/cover.png")
#    add_text_to_image("output/cover.png", "output/cover.png", "JULY 2025", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 62, (80,500), border_width=3, bold=True)
#    add_text_to_image("output/cover.png", "output/cover.png", "names", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48, (80,2000), border_width=3, max_width=1440, align="center", treat_as_names=True)
#    add_text_to_image("output/cover.png", "output/cover.png", "PLUS! A new issue of Samovar!", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 56, (290,2390), border_width=3, bold=True)
    template_files = os.listdir(TEMPLATE_DIR)
    for file in template_files:
        if file[-4:] == ".yml":
            book = WebBook(get_settings(file))
            book.write_book()

if __name__ == "__main__":
    main()
