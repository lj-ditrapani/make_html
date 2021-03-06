import unittest
import xml.etree.ElementTree as ET
import make_html


html_text = '''
<html>

<head></head>

<body>

<p>Before div</p>

<div>
    <p>In div, pre-content</p>
    <div id="content-marker"></div>
    <p>In div, post-content</p>
</div>

<p>After div</p>

</body>

</html>'''


html_no_content_marker_text = '''
<html>

<head></head>

<body>

<p>Before div</p>

<div>
    <p>In div, pre-content</p>
    <div id="content-marker-NOT!"></div>
    <p>In div, post-content</p>
</div>

<p>After div</p>

</body>

</html>'''


content_root_text = '''
<root>
<h1>Header</h1>
<p>1st para</p>
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
</ul>
</root>
'''

output_text = '''
<html>

<head></head>

<body>

<p>Before div</p>

<div>
    <p>In div, pre-content</p>
    <h1>Header</h1>
<p>1st para</p>
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
</ul>
<p>In div, post-content</p>
</div>

<p>After div</p>

</body>

</html>'''


class TestInsert(unittest.TestCase):

    def test_insert_nested_div(self):
        content_root = ET.fromstring(content_root_text)
        html = ET.fromstring(html_text)
        output = ET.fromstring(output_text)
        make_html.insert(content_root, html)
        self.assertEqual(ET.tostring(html).split('\n'),
                         ET.tostring(output).split('\n'))

    def test_insert_div_missing_content_marker(self):
        content_root = ET.fromstring(content_root_text)
        html = ET.fromstring(html_no_content_marker_text)
        with self.assertRaises(make_html.MakeHTMLError) as context:
            make_html.insert(content_root, html)
        self.assertEqual(
            context.exception.message,
            ('<div> tag with id="content-marker" not found in HTML ' +
             'template')
        )
