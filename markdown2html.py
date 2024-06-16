#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import os
import pathlib
import re
from sys import argv
import sys


def convert_md_to_html(md_file, html_file):
    with open(md_file, 'r') as md, open(html_file, 'w') as html:
        for line in md:
            match = re.match(r'((?:#){1,6}) (.*)', line.strip())
            if match:
                h_level = len(match.group(1))
                content = match.group(2)
                html.write(f'<h{h_level}>{content}</h{h_level}>\n')


if __name__ == '__main__':
    # Parse command-line arguments
    if len(argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html' ,file=sys.stderr)
        sys.exit(1)

    # Check if the input file exists
    input_path = argv[1]
    if not os.path.exists(sys.argv[1]):
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(argv[1], argv[2])
