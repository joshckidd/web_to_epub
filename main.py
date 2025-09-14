import settings
import requests
from parse import get_values
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def main():
    settings_dict = settings.get_settings()
    url = settings_dict["sources"]["link"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    values = get_values(soup, settings_dict["values"])
    # the line below doesn't work now because we're getting a regular string
    #values["content"].script.decompose()
    print(values["category"])
    print(values["author"])
    print(values["content"])
    print(values["title"])

if __name__ == "__main__":
    main()
