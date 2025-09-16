from settings import get_settings
from parse import get_values, get_links


def main():
    settings_dict = get_settings()
    # update for parsing links out of a page
    links = get_links(settings_dict["sources"])
    for url in links:
        values = get_values(url, settings_dict["values"])
        # update for possibilities like multiple categories
        print(values["category"])
        print(values["author"])
        print(values["content"])
        print(values["title"])

if __name__ == "__main__":
    main()
