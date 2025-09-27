import yaml
TEMPLATE_DIR = "template/"

def get_settings(file):
    with open(TEMPLATE_DIR + file, "r") as f:
        data = f.read()
    return yaml.safe_load(data)