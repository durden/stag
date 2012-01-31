#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import os
import argparse
import markdown
import string


def generate(src_dir, dest_dir):
    """Generate html from markdown files in src_dir and place in dest_dir"""

    md = markdown.Markdown()

    # Make sure directory has os dependent trailing slash
    src_dir = os.path.normpath(src_dir) + os.sep
    dest_dir = os.path.normpath(dest_dir) + os.sep

    for root, dirs, files in os.walk(src_dir):
        gen_dir = string.replace(root, root.split('/')[0], dest_dir)

        try:
            os.makedirs(gen_dir)
        except OSError:
            # Already exists
            pass

        for file_name in files:
            if not file_name.endswith(''.join([os.extsep, 'md'])):
                continue

            # Write to the same filename just swap .md for .html
            dest_file = ''.join([file_name.split(os.extsep)[0], os.extsep,
                                'html'])
            md.convertFile(os.path.join(root, file_name),
                           os.path.join(gen_dir, dest_file))


def main(content_dir):
    """main"""

    # Get all markdown files organized by subdirectory
    generate(args.content_dir, '_static')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument('content_dir', type=str,
                        help='Full path to main directory of markdown content')
    args = parser.parse_args()

    main(args.content_dir)
