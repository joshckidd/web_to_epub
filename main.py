import requests
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def main():
    URL = "http://strangehorizons.com/wordpress/poetry/watching-migrations/"
    page = requests.get(URL)
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
