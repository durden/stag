#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import argparse
import markdown
import os
import re


def generate(src_dir, dest_dir):
    """Generate html from markdown files in src_dir and place in dest_dir"""

    md = markdown.Markdown()

    if not os.path.isdir(src_dir):
        print "Source directory (%s) doesn't exist" % (src_dir)
        return 0

    # Make sure both paths are either absolute or relative
    if os.path.isabs(src_dir):
        dest_dir = os.path.abspath(dest_dir)
    else:
        dest_dir = os.path.relpath(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            if not file_name.endswith(''.join([os.extsep, 'md'])):
                continue

            # dest file will be same name/location with just dest_dir swapped
            # out for src_dir
            src_file = os.path.join(root, file_name)
            dest_file = re.sub(src_dir, dest_dir, src_file)

            # Write to the same filename just swap .md for .html
            dest_file = ''.join([dest_file.split(os.extsep)[0], os.extsep,
                                'html'])
            try:
                os.makedirs(os.path.dirname(dest_file))
            except OSError:
                # Already exists
                pass

            md.convertFile(src_file, dest_file)


def main():
    """main"""

    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument('content_dir', type=str,
                        help='Full path to main directory of markdown content')
    args = parser.parse_args()

    # Get all markdown files organized by subdirectory
    generate(args.content_dir, '_static')


if __name__ == "__main__":
    main()
