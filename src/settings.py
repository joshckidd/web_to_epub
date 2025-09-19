import yaml
# Use this for doc reference: https://pyyaml.org/wiki/PyYAMLDocumentation

def get_settings(testing=False):
    if testing:
        TEMPLATE_DIR = "template_test/"
    else:
        TEMPLATE_DIR = "template/"
    with open(TEMPLATE_DIR + "template.yml", "r") as f:
        data = f.read()
    return yaml.safe_load(data)