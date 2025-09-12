import settings
import requests
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def main():
    settings_dict = settings.get_settings()
    url = settings_dict["sources"]["link"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="post")
    category = results.find(rel="category").contents[0]
    author = results.find(class_="author").find("a").contents[0]
    content = results.find(class_="content")
    content.script.decompose()
    print(category)
    print(author)
    print(content)


if __name__ == "__main__":
    main()
