import os
import mimetypes
import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from ebooklib import epub
# Use this for doc reference: https://pypi.org/project/EbookLib/

class WebBook(epub.EpubBook):

    def __init__(self, settings_dict):
        super().__init__()
        self.spine = ["nav"]
        self.settings_dict = settings_dict
        self.__set_links()
        self.__set_values_order()
        self.__set_values_list()
        self.__set_ebook_values()
        self.__set_metadata()
        self.__set_templates()
        self.toc = []
        self.__set_sections()
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        self.__set_css()

    def write_book(self):
        # write to the file
        if "file-name" in self.ebook_values:
            epub.write_epub("output/" + self.ebook_values["file-name"][0], self, {})

    def __set_ebook_values(self):
        self.ebook_values = {}
        if "ebook-values" in self.settings_dict:
            values_settings = self.settings_dict["ebook-values"]
            for value in values_settings:
                new_values = []
                if "static" in values_settings[value]:
                    new_values.append(values_settings[value]["static"])
                if "aggregate" in values_settings[value]:
                    setting_split = values_settings[value]["aggregate"].split(" ", 1)
                    values = self.__get_all_values(setting_split[0])
                    if values != None:
                        new_values += self.__get_aggregate(setting_split[1], values)
                self.ebook_values[value] = new_values

    def __set_values_list(self):
        self.values_list = []
        for link in self.links:
            self.values_list.append(self.__get_values(link))

    def __set_links(self):
        self.links = []
        if "sources" in self.settings_dict:
            sources = self.settings_dict["sources"]
            if "links" in sources:
                self.links += sources["links"]
            if "link-pages" in sources:
                for link_page in sources["link-pages"]:
                    page = requests.get(link_page["url"])
                    soup = BeautifulSoup(page.content, "html.parser")
                    new_links = self.__parse_soup(soup, link_page["find"], link_page["url"])
                    absolute_links = list(map(lambda x: urljoin(link_page["url"], x), new_links))
                    self.links += absolute_links

    def __set_metadata(self):
        self.default_language = ""
        if "id" in self.ebook_values:
            self.set_identifier(self.ebook_values["id"][0])
        if "title" in self.ebook_values:
            self.set_title(self.ebook_values["title"][0])
        if "language" in self.ebook_values:
            self.set_language(self.ebook_values["language"][0])
            self.default_language = self.ebook_values["language"][0]
        if "authors" in self.ebook_values:
            for author in self.ebook_values["authors"]:
                self.add_author(author)

    def __set_templates(self):
        if "template-files" in self.settings_dict:
            template_files = self.settings_dict['template-files']
            if "chapter" in template_files:
                with open("template/" + template_files["chapter"], "r") as f:
                    self.chapter_template = f.read()
            if "css" in template_files:
                with open("template/" + template_files["css"], "r") as f:
                    self.css_template = f.read()
            if "section" in template_files:
                with open("template/" + template_files["section"], "r") as f:
                    self.section_template = f.read()

    def __create_chapters(self, section=None):
        chapter_list = []
        for values in self.values_list:
            if section == None or section in values[self.ebook_values["section-value"][0]]:
                title = ""
                if "chapter-title" in self.ebook_values and self.ebook_values["chapter-title"][0] in values:
                    title = values[self.ebook_values["chapter-title"][0]][0]
                c1 = epub.EpubHtml(title=title, file_name=title + ".xhtml", lang=self.default_language)
                c1.content = self.__merge_content(self.chapter_template, values)
                self.add_item(c1)
                chapter_list.append(c1)
        return chapter_list

    def __get_values(self, url):
        values = {}
        if "values" in self.settings_dict:
            values_settings = self.settings_dict["values"]
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            for value in self.values_order:
                new_values = []
                if "static" in values_settings[value]:
                    new_values.append(values_settings[value]["static"])
                if "find" in values_settings[value]:
                    new_values += self.__parse_soup(soup, values_settings[value]["find"], url)
                if "remove" in values_settings[value]:
                    new_values = list(map(lambda x: self.__remove_tags(x, values_settings[value]["remove"]), new_values))
                if "aggregate" in values_settings[value]:
                    setting_split = values_settings[value]["aggregate"].split(" ", 1)
                    if setting_split[0] in values:
                        new_values += self.__get_aggregate(setting_split[1], values[setting_split[0]])
                if "template" in values_settings[value]:
                    new_values.append(self.__merge_content(values_settings[value]["template"], values))
                values[value] = new_values                
            return values

    def __get_images(self, soup, url):
        images = soup.find_all("img")
        for image in images:
            source = image["src"]
            name = os.path.basename(urlparse(source).path)
            absolute_link = urljoin(url, source)
            image_content = requests.get(absolute_link).content
            mime_type, encoding = mimetypes.guess_type(name)
            img = epub.EpubImage(
                uid="image_" + name,
                file_name="static/" + name,
                media_type=mime_type,
                content=image_content,
            )
            self.add_item(img)
            image["src"] = "static/" + name
        return str(soup)

    def __get_aggregate(self, rule, values):
        rule_split = rule.split(" ", 1)
        if rule_split[0] == "join":
            if rule_split[1][0] == '"' and rule_split[1][-1] == '"':
                joiner = rule_split[1][1:-1]
            else:
                joiner = rule_split[1]
            return [joiner.join(values)]
        if rule_split[0] == "list":
            return values
        
    def __get_all_values(self, value):
        all_values = []
        for values in self.values_list:
            all_values += values[value]
        return all_values

    def __parse_soup(self, soup, find, url):
        # the rule can be a series of searches separated by a space
        # each section of the rule can be in the form <tag>.<attribute>
        find_split = find.split(" ", 1)
        results = self.__find_by_rule(soup, find_split[0])
        if len(find_split) == 1:
            for result in results:
                result = self.__get_images(result, url)
            return list(map(lambda x: str(x), results))
        elif find_split[1] == "text":
            return list(map(lambda x: x.get_text(), results))
        elif find_split[1][0:5] == "attr=":
            split_attr = find_split[1].split("=")
            return list(map(lambda x: x.attrs[split_attr[1]], results))
        new_results = []
        for result in results:
            new_results += self.__parse_soup(result, find_split[1], url)
        return new_results

    def __remove_tags(self, content, tag_list):
        soup = BeautifulSoup(content, "html.parser")
        for tag in tag_list:
            remove_list = self.__find_by_rule(soup, tag)
            if len(remove_list) != 0:
                for remove in remove_list:
                    remove.decompose()
        return str(soup)

    def __find_by_rule(self, soup, rule):
        if "." in rule:
            find_args = rule.split(".")
            results = soup.find_all(find_args[0], class_=find_args[1])
        elif "#" in rule:
            find_args = rule.split("#")
            results = soup.find_all(find_args[0], id=find_args[1])
        else:
            results = soup.find_all(rule)
        return results

    def __merge_content(self, template, values):
        content = template
        merge_fields = re.findall("{{([^}]*)}}", template)
        for merge_field in merge_fields:
            if merge_field in values:
                content = content.replace("{{" + merge_field + "}}", values[merge_field][0])
        return content

    def __set_values_order(self):
        self.values_order = []
        if "values" in self.settings_dict:
            values = self.settings_dict["values"]
            current_length = -1
            while current_length < len(self.values_order):
                current_length = len(self.values_order)
                for value in values:
                    if value not in self.values_order:
                        if "aggregate" not in values[value] and "template" not in values[value]:
                            self.values_order.append(value)
                        else:
                            dependencies = set()
                            if "aggregate" in values[value]:
                                dependencies.add(values[value]["aggregate"].split(" ", 1)[0])
                            if "template" in values[value]:
                                dependencies.update(re.findall("{{([^}]*)}}", values[value]["template"]))
                            met_dependencies = set()
                            for dependency in dependencies:
                                if dependency in self.values_order:
                                    met_dependencies.add(dependency)
                            if len(dependencies) == len(met_dependencies):
                                self.values_order.append(value)
            if len(self.values_order) < len(values):
                for value in values:
                    if value not in self.values_order:
                        self.values_order.append(value)

    def __set_css(self):
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=self.css_template,
        )
        self.add_item(nav_css)

    def __set_sections(self):
        new_toc = []
        if "sections" in self.ebook_values and "section-value" in self.ebook_values:
            for section in self.ebook_values["sections"][0]:
                self.ebook_values["current-section"] = [section]
                clist = self.__create_chapters(section=section)
                if len(clist) > 0:
                    s1page = epub.EpubHtml(uid=section, file_name=section + ".xhtml", content=self.__merge_content(self.section_template, self.ebook_values), title=section)
                    self.add_item(s1page)
                    self.spine.append(s1page)
                    s1 = epub.Section(section, href=section + ".xhtml")
                    self.spine += clist
                    self.toc.append([s1, clist])
        else:
            clist = self.__create_chapters()
            self.toc += clist
            self.spine += clist

