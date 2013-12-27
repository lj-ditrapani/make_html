import unittest
import xml.etree.ElementTree as ET
import make_html


html_text = '''
<html>
<head></head>
<body>
<p>Before</p>
</body>
</html>
'''


def mock_now():
    return '09 Sep 1999'


make_html.now = mock_now


class TestAddAuthorAndDate(unittest.TestCase):

    def setUp(self):
        self.html = ET.fromstring(html_text)

    def setup_test(self, author, date):
        config = dict(author=author, date=date)
        make_html.add_author_and_date(self.html, config)
        return list(self.html.find('body'))

    def run_test(self, author, date, expected_text):
        children = self.setup_test(author, date)
        self.assertEqual(len(children), 2)
        p = children[1]
        self.assertEqual(p.tag, 'p')
        self.assertEqual(p.attrib, {'class': 'footnote'})
        self.assertEqual(p.text, expected_text)
        self.assertEqual(p.tail, '\n\n')

    def test_add_nothing(self):
        children = self.setup_test('', '')
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].text, 'Before')

    def test_add_author_only(self):
        self.run_test('lj Di', '', 'Author:  lj Di ')

    def test_add_date_only(self):
        self.run_test('', '09 09 1999', '09 09 1999')

    def test_add_author_and_date(self):
        self.run_test('lj Di', '09 09 1999',
                      'Author:  lj Di 09 09 1999')

    def test_add_date_now(self):
        self.run_test('', 'now', '09 Sep 1999')

    def test_add_author_and_date_now(self):
        self.run_test('lj Di', 'now', 'Author:  lj Di 09 Sep 1999')
