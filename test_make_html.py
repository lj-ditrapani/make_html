#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import unittest, json, os
import xml.etree.ElementTree as ET
from compare_etrees import compare_etrees, XMLException
import make_html


class TestBibleVerse(unittest.TestCase):

    def setUp(self):
        os.chdir('bible_verse_input')

    def tearDown(self):
        os.chdir('..')
    
    def test_bible_verse(self):
        make_html.main()
        # Get expected output as etree
        expected_output = ET.parse(
            '../bible_verse_expected_output/test1.html')
        # Get actual output as etree
        '''
        actual_output = ET.parse(
            '../bible_verse_actual_ouptut/test1.html')
        '''
        # Compare 2
        # Remove newlines??

    def test_get_all_markdown_files(self):
        markdown_files = ['test1.markdown', 'test2.markdown']
        self.assertEqual(make_html.get_all_markdown_files(), markdown_files)


class TestCompareEtrees(unittest.TestCase):

    def run_failing_test(self, xml_str_1, xml_str_2, error_message):
        tree1 = ET.fromstring(xml_str_1)
        tree2 = ET.fromstring(xml_str_2)
        with self.assertRaises(XMLException) as context:
            compare_etrees(tree1, tree2, '/')
        self.assertEqual(str(context.exception), error_message)

    def run_passing_test(self, xml_str_1, xml_str_2):
        tree1 = ET.fromstring(xml_str_1)
        tree2 = ET.fromstring(xml_str_2)
        self.assertTrue(compare_etrees(tree1, tree2, '/'))
    
    def test_failing_etrees(self):
        tests = (
            ("<one></one>", "<two></two>",
             "Tags don't match at /: one two"),
            #(
            #    '<img src="abc" type="def"></img>',
            #    '<img type="def" src="xyz" ></img>',
            #    "Attributes don't match at /img: ...",
            #),
        )
        for str1, str2, message in tests:
            self.run_failing_test(str1, str2, message)

    def test_passing_etrees(self):
        tests = (
            ('<script></script>', '<script> </script>'),
            ('<script></script>', '<script />'),
            ('<script></script>', '<script>\n</script>'),
            ('<p><a> </a><b> </b></p>', '<p><a> </a><b> </b></p>'),
            (
                '<img src="abc" type="def"></img>',
                '<img type="def" src="abc" ></img>'
            ),
        )
        for str1, str2 in tests:
            self.run_passing_test(str1, str2)


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
