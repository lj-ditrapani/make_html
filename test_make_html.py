#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import os
import json
import unittest
import xml.etree.ElementTree as ET
import make_html


def fake_now():
    return '09 Sep 1999'


make_html.now = fake_now


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

    def tearDown(self):
        os.chdir('..')

    def test_config(self):
        expected_config = make_html.DEFAULTS.copy()
        expected_config['output_directory'] = (
            u'../bible_verse_actual_output')
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
        folder_config = make_html.get_folder_config()
        actual_config = make_html.get_file_config('test', folder_config)
        self.assertEqual(actual_config, expected_config)


if __name__ == '__main__':
    unittest.main()
