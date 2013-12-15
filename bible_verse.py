import xml.etree.ElementTree as ET

def main(html, config):
    body = html.find('body')
    for paragraph in body.findall('p'):
        if paragraph.get('verse') == None:
            continue
        span = ET.Element('span', {'class': 'reference'})
        span.text = '\n' + paragraph.get('verse') + '\n'
        span.tail = '\n' + paragraph.text
        paragraph.insert(0, span)
        paragraph.set('class', 'verse-box')
        del paragraph.attrib['verse']
        paragraph.text = None
