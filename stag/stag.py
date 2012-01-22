#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import os
import argparse


def main(content_dir):
    """main"""

    for root, dirs, files in os.walk(content_dir):
        for dir_name in dirs:
            if dir_name.startswith('.'):
                continue

        for file_name in files:
            if file_name.startswith('.'):
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument('content_dir', type=str,
                        help='Full path to main directory of markdown content')
    args = parser.parse_args()

    main(args.content_dir)
