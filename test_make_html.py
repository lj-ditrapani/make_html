#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import os
import unittest
import xml.etree.ElementTree as ET
import make_html
from test_insert import TestInsert
from test_add_author_and_date import TestAddAuthorAndDate


def mock_now():
    return '09 Sep 1999'


make_html.now = mock_now


def get_text(file_name):
    with open(file_name) as f:
        return f.read()


class TestBibleVerse(unittest.TestCase):

    def setUp(self):
        os.chdir('bible_verse_input')

    def tearDown(self):
        os.chdir('..')

    def make_folder_config(self):
        folder_config = make_html.DEFAULTS.copy()
        folder_config['output_directory'] = (
            u'../bible_verse_actual_output')
        folder_config['modules'] = [u'bible_verse']
        folder_config['author'] = u'Lyall Jonathan Di Trapani'
        return folder_config

    def test_bible_verse(self):
        self.maxDiff = None
        make_html.main()
        self.compare('test1.html')
        self.compare('test2.html')

    def compare(self, file_name):
        expected_string = get_text('../bible_verse_expected_output/' +
                                   file_name)
        actual_string = get_text('../bible_verse_actual_output/' +
                                 file_name)
        self.assertEqual(actual_string.split('\n'),
                         expected_string.split('\n'))

    def test_get_all_markdown_files(self):
        self.assertEqual(make_html.get_all_markdown_files(),
                         ['test1.markdown', 'test2.markdown'])

    def test_folder_config(self):
        expected_config = self.make_folder_config()
        actual_config = make_html.get_folder_config()
        self.assertEqual(actual_config, expected_config)

    def test_file_config(self):
        folder_config = self.make_folder_config()
        expected_config = folder_config.copy()
        expected_config['css'] = ['test2a.css', 'css/test2b.css']
        test2_json_contents = {
            "css": [u"test2a.css", u"css/test2b.css"],
            "javascript": [u"javascript/test2a.js", u"test2b.js"],
            u"bible": u"Amplified",
            "date": u"10 Dec 2013",
            "title": u"test2",
        }
        expected_config.update(test2_json_contents)
        actual_config = make_html.get_file_config('test2',
                                                  folder_config)
        self.assertEqual(actual_config, expected_config)


class TestConfig(unittest.TestCase):

    def setUp(self):
        os.chdir('config_test')
        self.defaults = make_html.DEFAULTS.copy()
        self.folder_config = make_html.get_folder_config()
        self.folder_config_copy = self.folder_config.copy()

    def tearDown(self):
        os.chdir('..')

    def test_config(self):
        expected_config = self.defaults
        expected_config['output_directory'] = (
            u'../bible_verse_actual_output'
        )
        expected_config['css'] = [u'css/a.css', u'b.css', u'test1.css',
                                  u'css/test2.css']
        expected_config['javascript'] = [u'js/a.js', u'js/b.js',
                                         u'js/test1.js', u'test2.js']
        expected_config['modules'] = [u'bible_verse', u'foo', u'bar']
        new_properties = {
            u'bible': u'Amplified',
            'date': u'10 Dec 2013',
            'title': u'From Config',
        }
        expected_config.update(new_properties)
        actual_config = make_html.get_file_config('test',
                                                  self.folder_config)
        self.assertEqual(actual_config, expected_config)

    def test_defaults_config_copy(self):
        self.assertEqual(self.folder_config['css'],
                         ['css/a.css', 'b.css'])
        self.assertEqual(make_html.DEFAULTS['css'], [])
        self.assertEqual(make_html.DEFAULTS, self.defaults)

    def test_folder_config_copy(self):
        folder_config = self.folder_config
        actual_config = make_html.get_file_config('test', folder_config)
        self.assertEqual(self.folder_config_copy['javascript'],
                         ['js/a.js', 'js/b.js'])
        self.assertEqual(actual_config['javascript'],
                         [u'js/a.js', u'js/b.js',
                          u'js/test1.js', u'test2.js'])
        self.assertEqual(folder_config, self.folder_config_copy)

    def test_file_config_missing(self):
        self.folder_config_copy['title'] = 'Test Title'
        file_config = make_html.get_file_config('test2',
                                                self.folder_config)
        self.assertEqual(file_config, self.folder_config_copy)

    def test_overwrite_title(self):
        file_config = make_html.get_file_config('test3',
                                                self.folder_config)
        self.assertEqual(file_config['title'], 'Overwritten Title')


class TestAddAttributes(unittest.TestCase):

    def run_test(self, input, output):
        root = ET.fromstring(input)
        make_html.add_attributes(root)
        self.assertEqual(ET.tostring(root), output)

    def test_add_attributes(self):
        input = ('\n<root>\n\n<p>{"id": "id1", "class": "class1"}\n' +
                 'The paragraph text</p>\n\n' +
                 '<p>Another paragraph</p>\n\n' +
                 '<p>{"key1": "val1", "key2": "val2"}\n' +
                 'The paragraph text</p>\n\n</root>')
        output = ('<root>\n\n<p class="class1" id="id1">' +
                  'The paragraph text</p>\n\n' +
                  '<p>Another paragraph</p>\n\n' +
                  '<p key1="val1" key2="val2">' +
                  'The paragraph text</p>\n\n</root>')
        self.run_test(input, output)

    def test_handle_p_with_no_text(self):
        root_text = '<root><p><a /></p></root>'
        self.run_test(root_text, root_text)


if __name__ == '__main__':
    unittest.main()
