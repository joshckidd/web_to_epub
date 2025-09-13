def get_values(soup, values_settings):
    # create a dictionary to hold the values that we will eventually plug into a template for 
    # the ebook
    values = {}
    # for every value setting that we have, parse the soup to find the correct value for that
    # setting
    for value in values_settings:
        values[value] = parse_soup(soup, values_settings[value])
    return values

def parse_soup(soup, value_rule):
    if value_rule == "contents":
        return soup.contents[0]
    value_rule_split = value_rule.split(" ", 1)
    find_args = value_rule_split[0].split(".")
    if len(find_args) == 1:
        new_soup = soup.find(find_args[0])
    else:
        kwargs = {find_args[0]: find_args[1]}
        new_soup = soup.find(**kwargs)
    if len(value_rule_split) == 1:
        return new_soup
    return parse_soup(new_soup, value_rule_split[1])