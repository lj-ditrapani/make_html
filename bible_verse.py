import xml.etree.ElementTree as ET


def main(html, config):
    body = html.find('body')
    fix_verses(body)
    add_bible_type(body, config)


def fix_verses(body):
    for paragraph in body.findall('p'):
        if paragraph.get('verse') is None:
            continue
        span = ET.Element('span', {'class': 'reference'})
        span.text = '\n' + paragraph.get('verse') + '\n'
        span.tail = '\n' + paragraph.text
        paragraph.insert(0, span)
        paragraph.set('class', 'verse-box')
        del paragraph.attrib['verse']
        paragraph.text = None


def add_bible_type(body, config):
    if 'bible' in config:
        body_elements = list(body)
        index = len(body_elements) - 1
        bible_note = ET.Element('p', {'class': 'footnote'})
        note = '(All verses from the {} Bible)'
        bible_note.text = note.format(config['bible'])
        bible_note.tail = '\n\n'
        body.insert(index, bible_note)
