make html
========================================================================

Creates html from markdown.  Translates all .markdown files in the current directory into HTML using the global config.json, file config.  Any json embedded in the markdown is used to add HTML attributes to the generated HTML.


File config json
----------------

Each `<filename>.markdown` can have an optional `<filename>.json`


HTML attributes in embedded json
--------------------------------

Block level (right now only `<p>` and `<pre>` tags) markdown elements can have json in the first line.


config.json
--------------

This is the global cofig file.  It is a json object.  Any of the fields can be omitted.  Actually, the entire file is optional.  If no config.json file is found in the current directory, the defaults values are used.

The valid fields along with their defaults are listed below:

- template: the file name of the HTML template
    - default:  template.html
- output\_directory: the directory where the final HTML files should be written to
    - default: . (current directory)
- css: list of css files to include in the `<head>`
    - default: []
- javascript:  list of javascript files to include in the `<head>`
    - default: []


Processing flow
---------------

    config.json
    <filename>.markdown
    <filename>.json
          |
          V
    --------------------------
    markdown2
    --------------------------
          |
          V
        HTML
          |
          V
    --------------------------
    json attr list processing
    --------------------------
          |
          V
    etree (+ attributes)
          |
          V
    --------------------------
    Post processing based on
    config.json and
    <filename>.json
    --------------------------
          |
          V
    <filename>.html


Dependencies
------------

Depends on python 2.7 and markdown2.

    sudo pip install markdown2


TODO
----

- Rename `compare_etrees` module to `etrees_utilities`?
- Should `compare_etrees` assume xml or html content?  In pure XML, white space in text matters.  In HTML, white space at beginning and end of text in block element doesn't matter (except in pre tags).  White space at beginning and end of in-line elements does matter.  Newlines and tabs are treated like spaces and multiple consecutive white space is treated like a single space.  All white space in pre tags matters.




Author:  Lyall Jonathan Di Trapani
