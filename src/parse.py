import requests
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def get_values(url, values_settings):
    values = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for value in values_settings:
        new_values = parse_soup(soup, values_settings[value]["find"])
        if "remove" in values_settings[value]:
            new_values = list(map(lambda x: remove_tags(x, values_settings[value]["remove"]), new_values))
        values[value] = new_values
    return values

def get_links(sources):
    links = []
    if "links" in sources:
        links += sources["links"]
    if "link-pages" in sources:
        for link_page in sources["link-pages"]:
            page = requests.get(link_page["url"])
            soup = BeautifulSoup(page.content, "html.parser")
            links += parse_soup(soup, link_page["pattern"])
    return links

def parse_soup(soup, value_rule):
    # the rule can be a series of searches separated by a space
    # each section of the rule can be in the form <tag>.<attribute>
    value_rule_split = value_rule.split(" ", 1)
    results = find_by_rule(soup, value_rule_split[0])
    if len(value_rule_split) == 1:
        return list(map(lambda x: str(x), results))
    elif value_rule_split[1] == "text":
        return list(map(lambda x: x.get_text(), results))
    elif value_rule_split[1][0:5] == "attr=":
        split_attr = value_rule_split[1].split("=")
        return list(map(lambda x: x.attrs[split_attr[1]], results))
    new_results = []
    for result in results:
        new_results += parse_soup(result, value_rule_split[1])
    return new_results

def remove_tags(content, tag_list):
    soup = BeautifulSoup(content, "html.parser")
    for tag in tag_list:
        remove_list = find_by_rule(soup, tag)
        if len(remove_list) != 0:
            for remove in remove_list:
                remove.decompose()
    return str(soup)

def find_by_rule(soup, rule):
    if "." in rule:
        find_args = rule.split(".")
        results = soup.find_all(find_args[0], class_=find_args[1])
    elif "#" in rule:
        find_args = rule.split("#")
        results = soup.find_all(find_args[0], id=find_args[1])
    else:
        results = soup.find_all(rule)
    return results