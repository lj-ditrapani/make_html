#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import json
import glob
import os
import datetime
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
    content_root = markdownToEtree(file_name)
    # parse attributes and add to content elements
    add_attributes(content_root)
    # or
    # add_attributes(content_root)
    # get template as etree
    tree = get_template(config)
    html = tree.getroot()
    # insert into template: root's children relpace div
    insert(content_root, html)
    fix_head(html, config)
    add_author_and_date(html, config)
    post_process(html, config)
    write_tree(tree, file_name, config)


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


def add_attributes(root):
    paragraphs = root.findall('p')
    for paragraph in paragraphs:
        first_line = paragraph.text.split('\n', 1)[0].strip()
        if first_line[0] == '{' and first_line[-1] == '}':
            paragraph.attrib = json.loads(first_line)
            index = paragraph.text.find('\n')
            paragraph.text = paragraph.text[index + 1:]


def get_template(config):
    tree = ET.parse(config['template'])
    tree.getroot().tail = '\n'
    return tree


def insert(content_root, html):
    # get children
    elements = list(content_root)
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


def fix_head(html, config):
    head = html.find('head')
    add_css_links(head, config['css'])
    add_javascript_links(head, config['javascript'])
    set_title(head, config['title'])


def set_title(head, title_text):
    title = ET.Element('title')
    title.text = title_text
    title.tail = '\n'
    head.append(title)


def add_css_links(head, css_file_names):
    for css_file_name in css_file_names:
        attrib = dict(href=css_file_name,
                      rel='stylesheet',
                      type='text/css')
        element = ET.Element('link', attrib)
        element.tail = '\n'
        head.append(element)


def add_javascript_links(head, javascript_file_names):
    for javascript_file_name in javascript_file_names:
        attrib = dict(type='text/javascript', src=javascript_file_name)
        element = ET.Element('script', attrib)
        element.text = ' '        # Forces an explicit closing tag
        element.tail = '\n'
        head.append(element)


def add_author_and_date(html, config):
    if config['author'] == '' and config['date'] == '':
        return
    author = config['author']
    if author != '':
        author = 'Author:  {} '.format(author)
    if config['date'] == 'now':
        date = now()
    else:
        date = config['date']
    text = author + date
    body = html.find('body')
    footnote = ET.SubElement(body, 'p', {'class': 'footnote'})
    footnote.text = text
    footnote.tail = '\n\n'


def now():
    return datetime.datetime.now().strftime('%d %b %Y')


def post_process(html, config):
    for module_name in config['modules']:
        module = __import__(module_name)
        module.main(html, config)


def write_tree(tree, file_name, config):
    out_dir = config['output_directory']
    html_file_name = '{}/{}.html'.format(out_dir, file_name)
    with open(html_file_name, 'w') as html_file:
        html_file.write(u'<!DOCTYPE html>\n')
        html_file.write(ET.tostring(tree.getroot()))


if __name__ == '__main__':
    main()
