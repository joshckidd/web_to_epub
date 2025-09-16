import requests
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def get_values(url, values_settings):
    values = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for value in values_settings:
        new_value = parse_soup(soup, values_settings[value]["find"])
        if "remove" in values_settings[value]:
            new_value = remove_tags(new_value, values_settings[value]["remove"])
        values[value] = new_value
    return values

def get_links(sources):
    links = []
    if "links" in sources:
        links += sources["links"]
    return links

def parse_soup(soup, value_rule):
    if value_rule == "text":
        return soup.get_text()
    # the rule can be a series of searches separated by a space
    # each section of the rule can be in the form <tag>.<attribute>
    value_rule_split = value_rule.split(" ", 1)
    new_soup = find_by_rule(soup, value_rule_split[0])
    if len(value_rule_split) == 1:
        return str(new_soup)
    return parse_soup(new_soup, value_rule_split[1])

def remove_tags(content, tag_list):
    soup = BeautifulSoup(content, "html.parser")
    for tag in tag_list:
        remove = find_by_rule(soup, tag)
        if remove != None:
            remove.decompose()
    return str(soup)

def find_by_rule(soup, rule):
    if "." in rule:
        find_args = rule.split(".")
        new_soup = soup.find(find_args[0], class_=find_args[1])
    elif "#" in rule:
        find_args = rule.split("#")
        new_soup = soup.find(find_args[0], id=find_args[1])
    else:
        new_soup = soup.find(rule)
    return new_soup