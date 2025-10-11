# web_to_epub

**Note: This tool may only be used to create ebooks from content where you are the copyright holder (e.g. the posts on your personal blog) or you have received explicit permission from the copyright holder to do so.**

## Project Description

A tool for scraping web content and generating an ebook from that content. Running main.py will look in the templates/ folder for any .yml files. For every well formed template file that it finds, it will generate an ebook in output/.

## Formatting Template Files

Template files include:

- A yaml file that describes how to scrape the content and generate the epub file
- Optional html templates for the ebook, as described in the yaml file
- An optional css file for the ebook, as described in the yaml file
- An optional cover image for the ebook, as described in the yaml file

The yaml file should include:

- A sources section that describes the urls to be scraped. For each url provided, a chapter will be generated in the ebook. The sources section should look something like this:

```yaml
sources:
  links:
    - https://joshckidd.github.io/static_site/blog/glorfindel/
  link-pages:
    - url: https://joshckidd.github.io/static_site/
      find: ul li a attr=href
```

- There are two optional sections under sources:
  - links - A list of URLs to be scraped
  - link-pages - A page from which we'll scrape URLs to be used. This includes a list of items with two values:
    - url - The url for the page to be scraped.
    - find - A find rule used for locating the links. The find rule uses css-like notation that provides a list of tags to search for on the page. '.' and '#' may be used to specify class or id attributes respectively. The scraper will search for the first tag within in the entire document, the second tag only within the results for the first tag, and so forth. For the last search item "text" may be specified to only return the text within the previous tag, or "attr=" may be specified to return a specific attribute for that tag. It will be quite common for find rules here to end in "attr=href".
- A values section that describes the what values should be extracted from a page for creating a chapter. Values listed here can be anything and can be named whatever you want. The values section should look something like this:

```yaml
values:
  title: 
    find: h1 text
  content:
    find: article div
    remove:
      - code
  author:
    static: Boots
  title-and-author:
    template: "{{title}} by {{author}}"
  category: 
    static: Blog Posts
  titles:
    aggregate: title join " and "
```

- The following optional sections can be defined for each value
  - find - These are used to scrape the page at the provided url for the values. And the find rule works identically here as it does for link-pages.
  - remove - This works in conjunction with the find section and removes any tags specified from the returned value.
  - change-tag - This works in conjunction with the find section and expects a list of items where one tag is separated by a space from another. The first tag will be changed to the second tag.
  - static - This specifies a static value.
  - template - This allows you to combine multiple other values in a templated way. It should be enclosed in quotes and merge fields should appear between {{}}. Merge fields can be any other values in the list.
  - aggregate - Since find rules can return multiple values, it can be helpful to aggregate the results. The first word indicates the value to be aggregated. The second indicates the type of aggregation to do. The third is an optional argument. The types of aggregation are:
    - join - Joins the values into a single string. The third argument is placed between all of the values.
    - list - Returns a list of all of the values. This is technically possible here, but not useful. This is more useful for ebook-values where it returns a list of values from across all chapters.
- An ebook-values section that describes values to be used across the whole ebook. Unlike the values section, there are specific values that can be set here. An ebook-values section should look something like this:

```yaml
  id: 
    static: uri:https://joshckidd.github.io/static_site/
  title:
    static: WebBook Test
  language:
    static: en
  file-name:
    static: test.epub
  titles:
    aggregate: title join " and "
  chapter-title:
    static: title-and-author
  cover:
    static: template_test.png
  section-value:
    static: category
  sections:
    static:
      - Blog Posts
```

- Currently only "static" and "aggregate" from above can be used as sections under ebook values. "aggregate" aggregates across all chapters.
  - An additional option "aggregate-section" can be used to aggregate values across sections. This expects two sub-items:
    - aggregate - Used exactly how aggregate is used above. But it wil be applied only to individual sections.
    - template - A template used for merging together the different sections. It expects two merge fields: {{section}} and {{aggregate}}
- The following values can be set as ebook-values:
  - id - Used to set the uid for the ebook.
  - title - Used to set the title for the ebook.
  - language - Used to set the language for the ebook.
  - publisher - Used to set the publisher for the ebook.
  - file-name - Used to specify the name for the ebook that is generated.
  - chapter-title - Used to indicate the chapter value that is used for the chapter title.
  - cover - Used to indicate the file for the cover image in the template\ folder.
  - section-value - Used to indicate the chapter value that will determine the section.
  - sections - A list of the sections to be used in the ebook.
  - Additional values may be defined here that can be used for page templates.
- A pages section that describes pages to be generated in addition to the generated chapters. The pages section should look something like this:

```yaml
pages:
  before-toc:
    - name: Title Page
      template: title
  before-sections:
    - name: Hello World
      template: hello-world
```

- There are two optional subsections in the pages section. They are:
  - before-toc: This contains a list of pages to be included before the table of contents that will not be in the table of contents. A title page is a good example of something you might want to include here.
  - before-sections: This contains a list of the pages to be included before the generated sections and chapters. These pages will be included in the table of contents.
- Each page should specify two elements:
  - name - The name for the page.
  - template - The template to be used for the page, as specified in the template-files section.
- A template-files section that describes templates to be used in the ebook. The template-files section should look something like this:

```yaml
template-files:
  chapter: template_test.html
  css: template_test.css
  section: template_test_section.html
  title: template_test_title.html
  hello-world: template_test_hw.html
```

- There are three standard subsections that can be defined here in addition to any custom templates referenced in the pages section. They are:
  - chapter - This file will define the template for individual chapters.
  - css - This is the css file that will be used for the ebook.
  - section - This file will define the template to be used for the page that begins each section.
  - Files for any other custom templates referenced in the pages section should also be specified.

The provided files in the template\ directory will create an ebook. Most of the features mentioned above are used in this template. I invite you to copy the files and play around with them to see what's possible. Keeping the original files as they are is needed for the tests to work.

## Planned Updates

- Adding support for accessibility tags.
- Adding support for additional ebook metadata.
- Adding support for pages after the sections.
