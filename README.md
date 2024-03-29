#Stag

A dead-simple static site generator in Python.

##Install and run

    1. Get code: git clone git://github.com/durden/stag.git
    2. Install requirements: pip install -r requirements.txt
    3. Install project: pip install .
    4. Run tests: nosetests stag/
    5. Get help: stag --help
    6. Generate site: stag <my_content_directory>

###Goals

The main goal of stag is to be simple enough to use and digest with minimal
hand holding.  I (like lots of developers) am really attracted to the idea of
writing blogs/websites in just regular text.

Not all websites need a database.  My perosnal site is a great example.  I
simply want a place to post articles about the projects I'm working on and tell
the world a little about me.  In order to do this I want to take down any extra
walls that keep me from doing this effictively and often.

HTML is the basis for all web content.  This is a hierarchial format with all
content a child of the <html> element.  File system layouts are also
hierarchial in nature.  Thus, it makes sense to use all the meta information
from the file system (timestamps, directory layout, etc.) to build a website.

Stag strives to require very little configuration from the user and is built in
the 'convention over configuration' development style.

###Requirements

I prefer to write in vim and markdown.  So, I want to build this entire project
with only a single external dependency, markdown.  It might be nice later to
add support for a templating engine like jinja, etc.  However, I want to see if
I can get by with even less first.


####Usage

Stag is meant to be run with a single argument, the root directory of the
markdown files that will provide the site content.

Stag assumes the following information about the root directory, layout, etc.:

- Any directories/files starting with '.' are ignored.
- Only files with .md or .markdown extensions are considered markdown files.
- Only markdown files will be transformed into html.
- All non-markdown files will be copied into the static site without changes.
- All markdown files at the root directory will be treated as the main parts of
  the website.
- If a directory does not have an index.html file, one will be generated for it
  that will simply contain a list of all the 'articles' aka files under the
  directory.
- Each subdirectory is treated as a subset of the main website.
- Each subdirectory will be represented as a page with links to all it's
  child elements (files within the directory).
- Articles (posts) will be ordered according to the file timestamp.
- Title of all pages will be determined from the file name with the following
  transformations:
    - '_' characters will be changed to ' ' (space) for page titles
    - '_' characters will be changed to '-' for all page links
  output.

These assumptions are best explained with a simple example.  Given the
following directory layout (assume sorted by timestamp, newest first):

    mysite/
        about.markdown
        contact.markdown
        mysite.markdown
        blog/
            new_article.markdown
            article3.markdown
            article2.markdown
            article1.markdown

This directory will yield a website with the following link layout:

    /index.html
    /about.html
    /contact.html
    /blog/index.html (Contains links for all articles)
        /blog/new-article.html
        /blog/article3.html
        /blog/article2.html
        /blog/article1.html
