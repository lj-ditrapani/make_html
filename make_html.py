#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import json, glob
import xml.etree.ElementTree as ET

DEFAULTS = dict(
    template='template.html',
    output_directory='.',
    css=[],
    javascript=[],
)


def get_text(file_name):
    with open(file_name) as f:
        return f.read()


def main():
    config = get_folder_config()
    for file_name in get_all_markdown_files():
        convert(file_name, config)


def get_folder_config():
    config = DEFAULTS.copy()
    json_config = json.load(open('config.json', 'U'))
    config.update(json_config)
    return config


def get_all_markdown_files():
    return glob.glob("*.markdown")


def convert(file_name, folder_config):
    pass


def get_file_config(file_name, folder):
    text = get_text('{}/{}.markdown'.format(folder, file_name))
    title = text.split('\n', 1)[0].strip()
    config = dict(
        title=title,
        css=[],
        javascript=[],
        prettyprint=False,
    )
    json_file_name = '{}/{}.json'.format(folder, file_name)
    if os.path.exists(json_file_name):
        json_config = json.load(open(json_file_name, 'U'))
        config.update(json_config)
    return config
