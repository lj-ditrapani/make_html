make html
========================================================================

Creates html from markdown.
Translates all .markdown files in the current directory into HTML.
Configuration and processing directives are specified in json.
There is an optional folder-level configuration file, config.json,
as well as optional per-file configuration files (also json).
Any json embedded in the markdown is used to add HTML attributes to the
generated HTML.


HTML attributes in embedded json
--------------------------------

Block level (right now only `<p>` and `<pre>` tags) markdown elements
can have json in the first line.
The json must be a single object with strings for all keys and all
values.
The object's properties will become the HTML element's attributes.
For example, the following markdown

    {"id": "id001", "class": "class01"}
    The paragraph text

        {"class": "prettyprint"}
        function squar(x) {
            return x * x;
        }

will translate to the following HTML:

    <p id="id001" class="class01">
    The paragraph text
    </p>

    <pre class="prettyprint"><code>
    function squar(x) {
        return x * x;
    }
    </code></pre>


Per-file Configuration (json)
-----------------------------

Each `<filename>.markdown` can have an optional `<filename>.json`
configuration file.  The file contains a single json object.

The basic properties of the json object along with their default values
are listed below:

- css: list of css files to include in the `<head>`
    - default: []
- javascript:  list of javascript files to include in the `<head>`
    - default: []
- modules:  list of python modules to run post-processing on the
  generated etree before it is written out to the final output HTML
  file.  Each python module must have a `main(tree, config)` function
  that hase two parameters.  The first parameter is the etree created
  from the markdown and the second parameter is a dictionary of the
  combined folder-level configuration and per-file configuration.
  The python modules must already be on the python path.  The
  `make_html.py` script will load each python module specified and
  invoke the `main(tree, config)` function of each module.
    - default: []
- author:  string
    - default: "" (the empty string)
- date:  string; can be any format.  If "now" is specefied, the current
  date is used.
    - default: "now"

If you are using the `"modules"` properties to do post-processing,
you can include information to be passed along to your module(s) in the
configuration file.  Therefore, the json file can contain any arbitrary
properties and values.  The `make_html.py` script will simply ignore
the extra properties and pass them along to the additional Python
modules you have specified.

If the css property is present in both the folder-level configuration
file, config.json, and the per-file configuration file,
the css lists are combined
and all css files specified in both files are included in the `<head>`
of the output html file.  This is also true for the javascript property.

If the modules filed is present in both the folder-level configuration
file, config.json, and the per-file configuration file, the module
lists are combined and all modules specified in both files are executed.

Example per-file configuration file:
If you had a file example.markdown, the optional example.json file
might look like the following.

    {
        "css": ["base.css", "index.css"],
        "javascript": ["jquery.js", "index.js"],
        "date": "2013 Dec 25",
        "author": "Joe Blow",
        "modules": ["add_dynamic", "generate_table"]
    }


Folder-level Configuration:  config.json
----------------------------------------

This is the folder-level configuration file.
The file is optional.
It is a single json object.
Any of the properties of the object can be omitted.
If no config.json file is found in the current directory,
the defaults values are used.

All properties specified in the _Per-file Configuration_ section are
also valid folder-level configuration properties.
In additon to the previous properties,
properties specific to the config.json
file are listed below:

- template: the file name of the HTML template
    - default:  template.html
- output\_directory: the directory where the final HTML files should be
  written to
    - default: . (current directory)


Processing flow
---------------

    config.json (folder-level configuration, optional)
    <filename>.markdown
    <filename>.json (per-file configuration, optional)
               ||
               \/
    --------------------------------
            markdown2
    --------------------------------
               ||
               \/
              HTML
               ||
               \/
    --------------------------------
       json attr list processing
    --------------------------------
               ||
               \/
        etree (+ attributes)
               ||
               \/
    --------------------------------
    Post processing based on python
    modules and properties specified
    in config.json and
    <filename>.json
    --------------------------------
               ||
               \/
        <filename>.html


Dependencies
------------

Depends on python 2.7 and markdown2.

    sudo pip install markdown2






Author:  Lyall Jonathan Di Trapani
