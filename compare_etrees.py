class XMLException(Exception):
    pass


def compare_etrees(element1, element2, path):
    new_path = path + '/' + element1.tag
    if element1.tag != element2.tag:
        msg = "Tags don't match at {}: {} {}"
        raise XMLException(msg.format(path, element1.tag, element2.tag))
    return True
