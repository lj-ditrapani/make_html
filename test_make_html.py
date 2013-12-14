#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import unittest, json, os
import xml.etree.ElementTree as ET
import make_html


def get_text(file_name):
    with open(file_name) as f:
        return f.read()


class TestBibleVerse(unittest.TestCase):

    def setUp(self):
        os.chdir('bible_verse_input')

    def tearDown(self):
        os.chdir('..')
    
    def test_bible_verse(self):
        make_html.main()
        expected_string = get_text(
            '../bible_verse_expected_output/test1.html')
        actual_string = get_text(
            '../bible_verse_actual_ouptut/test1.html')
        self.assertEqual(actual_string, expected_string)
        expected_string = get_text(
            '../bible_verse_expected_output/test2.html')
        actual_string = get_text(
            '../bible_verse_actual_ouptut/test2.html')
        self.assertEqual(actual_string, expected_string)

    def test_get_all_markdown_files(self):
        self.assertEqual(make_html.get_all_markdown_files(),
                         ['test1.markdown', 'test2.markdown'])

    def test_folder_config(self):
        expected_config = make_html.DEFAULTS.copy()
        expected_config['output_directory'] = u'../bible_verse_actual_output'
        expected_config[u'modules'] = [u'bible_verse']
        actual_config = make_html.get_folder_config()
        self.assertEqual(actual_config, expected_config)


class TestFileConfig(unittest.TestCase):

    def test_parse_paragraph(self):
        tests = ((), ())


if __name__ == '__main__':
    unittest.main()
