import yaml
# Use this for doc reference: https://pyyaml.org/wiki/PyYAMLDocumentation

TEMPLATE_DIR = "template/"

def get_settings():
    with open(TEMPLATE_DIR + "template.yml", "r") as f:
        data = f.read()
    return yaml.safe_load(data)