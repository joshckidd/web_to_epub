from src.settings import get_settings
from src.parse import get_values, get_links

# add tests

def main():
    settings_dict = get_settings()
    links = get_links(settings_dict["sources"])
    for url in links:
        values = get_values(url, settings_dict["values"])
        print(values["category"])
        print(values["author"])
        print(values["content"])
        print(values["title"])

if __name__ == "__main__":
    main()
