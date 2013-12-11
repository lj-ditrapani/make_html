#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import unittest, json, os
import xml.etree.ElementTree as ET
import make_html


class TestBibleVerse(unittest.TestCase):

    def setUp(self):
        os.chdir('bible_verse_input')

    def tearDown(self):
        os.chdir('..')
    
    def test_bible_verse(self):
        make_html.main()
        # Get expected output as etree
        with open('../bible_verse_expected_output/test1.html') as f:
            expected_output = f.read()
        print expected_output[0:30]
        # Get actual output as etree
        # Compare 2
        # Remove newlines??

    def test_get_all_markdown_files(self):
        markdown_files = ['test1.markdown', 'test2.markdown']
        self.assertEqual(make_html.get_all_markdown_files(), markdown_files)



class TestFolderConfig(unittest.TestCase):

    def test_get_date(self):
        tests = (('12 Feb 2013', True),
                 ('12 feb 2013', False),
                 ('12 March 2013', False),
                 ('12 Mar 13', False))


class TestFileConfig(unittest.TestCase):

    def test_parse_paragraph(self):
        tests = ((), ())


if __name__ == '__main__':
    unittest.main()
