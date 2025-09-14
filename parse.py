def get_values(soup, values_settings):
    values = {}
    for value in values_settings:
        values[value] = parse_soup(soup, values_settings[value])
    return values

def parse_soup(soup, value_rule):
    if value_rule == "text":
        return soup.get_text()
    # the rule can be a series of searches separated by a space
    # each section of the rule can be in the form <tag>.<attribute>
    value_rule_split = value_rule.split(" ", 1)
    find_args = value_rule_split[0].split(".")
    if len(find_args) == 1:
        new_soup = soup.find(find_args[0])
    else:
        kwargs = {find_args[0]: find_args[1]}
        new_soup = soup.find(**kwargs)
    if len(value_rule_split) == 1:
        return str(new_soup)
    return parse_soup(new_soup, value_rule_split[1])