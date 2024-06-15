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

import sys
import markdown

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py [input_file] [output_file]")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(markdown_file, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"Missing '{markdown_file}'\n")
        sys.exit(1)

    html = markdown.markdown(text)

    with open(output_file, 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()