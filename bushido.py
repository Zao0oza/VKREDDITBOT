import yaml
from os import getcwd, path, makedirs

with open('C:\mainbot\settings.yaml', encoding='utf-8') as f:
    templates = yaml.safe_load(f)

    print(templates['dictionary'])

