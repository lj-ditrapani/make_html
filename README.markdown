make html
========================================================================

Creates html from markdown.
Translates all .markdown files in the current directory into HTML.
Configuration and processing directives are specified in json.
There is an optional folder-level configuration file, config.json,
as well as optional per-file configuration files (also json).
Any json embedded in the markdown is used to add HTML attributes to the
generated HTML.  User-defined post processing is done on a
xml.etree.ElementTree object generated from the markdown.


Folder-level Configuration:  config.json
----------------------------------------

This is the folder-level configuration file.
The file is optional.
It is a single json object.
Any of the properties of the object can be omitted.
If no config.json file is found in the current directory,
the defaults values are used.

The basic properties of the json object along with their default values
are listed below:

- template: the file name of the HTML template
    - default:  `"template.html"`
- output\_directory: the directory where the final HTML files should be
  written to
    - default: `"."` (current directory)
- css: list of css files to include in the `<head>`
    - default: `[]`
- javascript:  list of javascript files to include in the `<head>`
    - default: `[]`
- author:  string
    - default: `""` (the empty string)
- date:  string; can be any format.  If "now" is specefied, the current
  date is used.
    - default: `"now"`
- modules:  list of python modules to run post-processing on the
  generated xml.etree.ElementTree before it is written out to the
  final output HTML file.
    - default: `[]`

All of the above properties are
also valid per-file configuration properties except for the
`"template"` and `"output_directory"` properties.

If you are using the `"modules"` properties to do post-processing,
you can include information to be passed along to your module(s) in the
configuration file.  Therefore, the json file can contain any arbitrary
properties and values.  The `make_html.py` script will simply ignore
the extra properties and pass them along to the additional Python
modules you have specified.

An example config.json file:

    {
        "template": "../templates/blog_template.html",
        "output_directory": "../www",
        "css": ["css/prettify.css"],
        "javascript": ["js/prettify.js"],
        "modules": ["transform_lists.py"]
    }


Per-file Configuration (json)
-----------------------------

Each `<filename>.markdown` can have an optional `<filename>.json`
configuration file.  The file contains a single json object.

All properties specified in the _Folder-level Configuration_ section are
also valid per-file configuration properties except for the
`"template"` and `"output_directory"` properties.
The `"template"` and `"output_directory"` properties are specific to the
config.json file.

As with the folder-level configuration file, config.json, the per-file
configuration files can also contain any arbitrary properties and
values to be used by any included python modules for post-processing.

The per-file configuration files inherit the properties of the
folder-level config.json file.  The properties of the two files are
combined to create a single configuration dictionary.

If the css property is present in both the folder-level configuration
file, config.json, and the per-file configuration file,
the css lists are combined
and all css files specified in both files are included in the `<head>`
of the output html file.  This is also true for the javascript property.

If the modules property is present in both the folder-level
configuration file, config.json,
and the per-file configuration file, the module
lists are combined and all modules specified in both files are executed.

All other properties that are specified in both config.json and the 
per-file configuration file are overridden by the per-file configuration
file.  This way, you can specify properties that apply to most of your
files in the folder-level config.json file, and handle special cases
by over-ridding the property in the per-file configuration file.

Example per-file configuration file:
If you had a file `example.markdown`, the optional `example.json` file
might look like the following.

    {
        "css": ["base.css", "index.css"],
        "javascript": ["jquery.js", "index.js"],
        "date": "2013 Dec 25",
        "author": "Joe Blow",
        "modules": ["add_dynamic", "generate_table"]
    }


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

        {"class": "prettyprint linenums"}
        function square(x) {
            return x * x;
        }

will translate to the following HTML:

    <p id="id001" class="class01">
    The paragraph text
    </p>

    <pre class="prettyprint linenums"><code>
    function square(x) {
        return x * x;
    }
    </code></pre>


HTML Templates
--------------

A template file should be valid HTML and XML.
It must contain a `<div>` element with an id of `"content-marker"`.
The `make_html.py` script completely removes and replaces the `<div>`
element with the HTML elements generated from the markdown input file.

Do not manually place content inside the `"content-marker"` `<div>`
tag of the HTML template file.
The `<div>` element will be completely removed.  
The `<div>` tag simply acts as a marker where the content should be
placed.
It will not be part of the final HTML file.


Post-processing Modules
-----------------------

The `"modules"` configuration property specifies a list of python
modules to run post-processing on the generated xml.etree.Element
before it is written out to the final output HTML file.
Each python module must have a `main(html, config)` function
that has two parameters.
The first parameter is the xml.etree.Element created from the
markdown (it is an HTML tag) and the
second parameter is a dictionary of the combined folder-level
configuration and per-file configuration.
The `main` function returns None, therefor, the xml.etree.Element
object must be modified in-place by the `main()` function.

`main` function signature:

    Element X dictionary -> None

The python modules must already be on the python path.
The `make_html.py` script will load each python module specified and
invoke the `main(tree, config)` function of each module.
The modules are executed in the order they are declared in the
configuration files.  Modules declared in the folder-level
`config.json` file are executed before any modules declared in the
per-file configuration.


Title
-----

The first line of the markdown file becomes the `<title>` set in the
HTML `<head>` tag.  This can be overridden by specifying a `"title"`
property in the per-file configuration file, which will be used as
the `<head>` title instead of the first line in the markdown file.


Processing flow
---------------

    config.json (folder-level configuration, optional)
    <filename>.json (per-file configuration, optional)
    <filename>.markdown
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
      etree Element (+ attributes)
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


TODO
----

- Add "_disable attribute parsing_" configuration property
- Add alternate input directory configuration property
- Add alternate config.json folder path command line argument
- Add more tests 
- Add tests for corner cases
- Add descriptive exceptions to make it more user friendly & tests
- Create WomenOfVictory acceptance tests
- Create MyLittleConqueror acceptance tests
- Create MyLittleConqueror2 acceptance tests
- Update Sofi's sites to use this
- Create SWE 430 acceptance tests
- Replace SWE 430 code to use this instead
- When run, check timestamps and only process files that are
  out-of-date.

Ex:

    if time_of(.markdown) > time_of(.html)
        process
    else
        skip

- Make it nestable; multiple nested templates
    - Separate function that writes the final output from function that
      does all the other work.
    - This way, can call convert function and just return the etree
      without writting it out to file.
    - Function that writes out final output also adds `<!DOCTYPE html>`.
    - javascript and css properties only valid for outermost file config
      and folder-level config.json



Author:  Lyall Jonathan Di Trapani
