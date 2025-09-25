import requests
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
# Use this for doc reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def get_values(url, values_settings):
    values = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for value in values_settings:
        new_values = []
        if "static" in values_settings[value]:
            new_values.append(values_settings[value]["static"])
        if "find" in values_settings[value]:
            new_values += parse_soup(soup, values_settings[value]["find"])
        if "remove" in values_settings[value]:
            new_values = list(map(lambda x: remove_tags(x, values_settings[value]["remove"]), new_values))
        if "images" in values_settings[value]:
            new_values = list(map(lambda x: get_images(x, values_settings[value]["images"]), new_values))
        values[value] = new_values
    for value in values:
        if "aggregate" in values_settings[value]:
            setting_split = values_settings[value]["aggregate"].split(" ", 1)
            if setting_split[0] in values:
                values[value] += get_aggregate(setting_split[1], values[setting_split[0]])
    return values

def get_values_list(links, values_settings):
    values_list = []
    for link in links:
        values_list.append(get_values(link, values_settings))
    return values_list

def get_ebook_values(values_list, values_settings):
    ebook_values = {}
    for value in values_settings:
        new_values = []
        if "static" in values_settings[value]:
            new_values.append(values_settings[value]["static"])
        if "aggregate" in values_settings[value]:
            setting_split = values_settings[value]["aggregate"].split(" ", 1)
            values = get_all_values(values_list, setting_split[0])
            if values != None:
                new_values += get_aggregate(setting_split[1], values)
        ebook_values[value] = new_values
    return ebook_values


def get_links(sources):
    links = []
    if "links" in sources:
        links += sources["links"]
    if "link-pages" in sources:
        for link_page in sources["link-pages"]:
            page = requests.get(link_page["url"])
            soup = BeautifulSoup(page.content, "html.parser")
            new_links = parse_soup(soup, link_page["find"])
            absolute_links = list(map(lambda x: urljoin(link_page["url"], x), new_links))
            links += absolute_links
    return links

def get_images(content, folder):
    if folder == None:
        folder = ""
    soup = BeautifulSoup(content, "html.parser")
    images = soup.find_all("img")
    for image in images:
        source = image["src"]
        name = os.path.basename(urlparse(source).path)
        page = requests.get(source)
        Path("output/" + folder).mkdir(parents=True, exist_ok=True)
        with open("output/" + folder + name, "wb") as f:
            f.write(page.content)
        image["src"] = "static/" + name
    return str(soup)

def get_aggregate(rule, values):
    rule_split = rule.split(" ", 1)
    if rule_split[0] == "join":
        if rule_split[1][0] == '"' and rule_split[1][-1] == '"':
            joiner = rule_split[1][1:-1]
        else:
            joiner = rule_split[1]
        return [joiner.join(values)]
    if rule_split[0] == "list":
        return values
    
def get_all_values(values_list, value):
    all_values = []
    for values in values_list:
        all_values += values[value]
    return all_values

def parse_soup(soup, find):
    # the rule can be a series of searches separated by a space
    # each section of the rule can be in the form <tag>.<attribute>
    find_split = find.split(" ", 1)
    results = find_by_rule(soup, find_split[0])
    if len(find_split) == 1:
        return list(map(lambda x: str(x), results))
    elif find_split[1] == "text":
        return list(map(lambda x: x.get_text(), results))
    elif find_split[1][0:5] == "attr=":
        split_attr = find_split[1].split("=")
        return list(map(lambda x: x.attrs[split_attr[1]], results))
    new_results = []
    for result in results:
        new_results += parse_soup(result, find_split[1])
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