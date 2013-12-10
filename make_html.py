#!/usr/bin/env python
# Author:  Lyall Jonathan Di Trapani -----------------------------------
import json, glob
import xml.etree.ElementTree as ET

DEFAULTS = dict(
    template='boilerplate.html',
    output_directory='.',
    css=[],
    javascript=[],
)


def main():
    for file_name in get_all_markdown_files():
        convert(file_name)


def get_all_markdown_files():
    return glob.glob("*.markdown")


def convert(file_name):
    pass
