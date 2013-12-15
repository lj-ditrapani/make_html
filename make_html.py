#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import json
import glob
import os
import xml.etree.ElementTree as ET
import markdown2


DEFAULTS = dict(
    template='template.html',
    output_directory='.',
    css=[],
    javascript=[],
    author='',
    date='now',
    modules=[],
)


def get_text(file_name):
    with open(file_name) as f:
        return f.read()


def main():
    config = get_folder_config()
    for markdown_file_name in get_all_markdown_files():
        file_name, ext = os.path.splitext(markdown_file_name)
        convert(file_name, config)


def get_folder_config():
    config = DEFAULTS.copy()
    json_config = json.load(open('config.json', 'U'))
    config.update(json_config)
    return config


def get_all_markdown_files():
    return glob.glob("*.markdown")


def convert(file_name, folder_config):
    config = get_file_config(file_name, folder_config)
    element = markdownToEtree(file_name)
    # parse attributes and add to root element
    # element = add_attributes(element)
    # or
    # add_attributes(element)
    # get template as etree
    html = get_template(config)
    html.getroot().tail = '\n'
    # insert into template: root's children relpace div
    insert(element, html)
    write_tree(html, file_name, config)


def get_file_config(file_name, config):
    text = get_text('{}.markdown'.format(file_name))
    title = text.split('\n', 1)[0].strip()
    config['title'] = title
    json_file_name = '{}.json'.format(file_name)
    if os.path.exists(json_file_name):
        json_config = json.load(open(json_file_name, 'U'))
        for key, val in json_config.items():
            if key in ['css', 'javascript', 'modules']:
                config[key] = config[key] + val
            else:
                config[key] = val
    return config


def markdownToEtree(file_name):
    markdown_text = get_text('{}.markdown'.format(file_name))
    html_text = markdown2.markdown(markdown_text)
    return ET.fromstring('<root>\n{}\n</root>\n'.format(html_text))


def get_template(config):
    return ET.parse(config['template'])


def insert(element, html):
    # get children
    elements = list(element)
    body = html.find('body')
    body_children = list(body)
    divs = body.findall('div')
    content_marker_div = ''
    for div in divs:
        if div.attrib == {'id': 'content-marker'}:
            content_marker_div = div
    # if content_marker_div not found, raise error
    if content_marker_div == '':
        raise Exception('content_marker_div not found!')
    # find index of content_marker_div in body_children list
    index = body_children.index(content_marker_div)
    # use body.insert for each element in elements
    for element in elements:
        index += 1
        body.insert(index, element)
    body.remove(content_marker_div)


def write_tree(tree, file_name, config):
    out_dir = config['output_directory']
    html_file_name = '{}/{}.html'.format(out_dir, file_name)
    with open(html_file_name, 'w') as html_file:
        html_file.write(u'<!DOCTYPE html>\n')
        html_file.write(ET.tostring(tree.getroot()))
