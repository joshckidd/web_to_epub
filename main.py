import settings
import requests
from parse import get_values


def main():
    settings_dict = settings.get_settings()
    url = settings_dict["sources"]["link"]
    page = requests.get(url)
    values = get_values(page.content, settings_dict["values"])
    print(values["category"])
    print(values["author"])
    print(values["content"])
    print(values["title"])

if __name__ == "__main__":
    main()
