class XMLException(Exception):
    pass


def compare_etrees(element1, element2, path=''):
    new_path = path + '/' + element1.tag
    if path == '':
        path = '/'
    if element1.tag != element2.tag:
        msg = "Tags don't match at {}: {} {}"
        raise XMLException(msg.format(path, element1.tag, element2.tag))
    if element1.attrib != element2.attrib:
        format = "Attributes don't match at {}: {} {}".format
        message = format(new_path, element1.attrib, element2.attrib)
        raise XMLException(message)
    print element1.text
    print element1.tail
    print list(element1)
    return True
