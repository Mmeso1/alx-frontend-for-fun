#!/usr/bin/env python3
""" Converts a Markdown file to HTML """

import sys
import os
import re
import hashlib


def convert_md_to_html(md_file, html_file):
    """ Converts a Markdown file to HTML """
    # Define the markdown syntaxes and their corresponding HTML conversion functions
    syntaxes = [
        (r'((?:#){1,6}) (.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>\n'),
        (r'\* (.*)', lambda m: f'<li>{m.group(1)}</li>\n'),  # Ordered list
        (r'- (.*)', lambda m: f'<li>{m.group(1)}</li>\n'),  # Unordered list
        (r'\*\*(.*?)\*\*', lambda m: f'<b>{m.group(1)}</b>'),  # Bold text
        (r'__(.*?)__', lambda m: f'<em>{m.group(1)}</em>'),  # Emphasized text
        (r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest()),  # MD5 conversion
        (r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', '')),  # Remove 'c' or 'C'
    ]

    def process_line(line):
        for regex, converter in syntaxes:
            line = re.sub(regex, converter, line)
        return line

    with open(md_file, 'r') as md, open(html_file, 'w') as html:
        in_ordered_list = False
        in_unordered_list = False
        in_paragraph = False
        paragraph_lines = []

        for line in md:
            stripped_line = line.strip()
            matched = False

            if not stripped_line:
                if in_paragraph:
                    html.write('<p>\n' + '<br/>\n'.join(paragraph_lines) + '\n</p>\n')
                    paragraph_lines = []
                    in_paragraph = False
                continue

            for regex, converter in syntaxes[:3]:  # Only header and list processing
                match = re.match(regex, stripped_line)
                if match:
                    if in_paragraph:
                        html.write('<p>\n' + '<br/>\n'.join(paragraph_lines) + '\n</p>\n')
                        paragraph_lines = []
                        in_paragraph = False

                    if regex == r'\* (.*)':
                        if not in_ordered_list:
                            if in_unordered_list:
                                html.write('</ul>\n')
                                in_unordered_list = False
                            html.write('<ol>\n')
                            in_ordered_list = True
                        html.write(converter(match))
                    elif regex == r'- (.*)':
                        if not in_unordered_list:
                            if in_ordered_list:
                                html.write('</ol>\n')
                                in_ordered_list = False
                            html.write('<ul>\n')
                            in_unordered_list = True
                        html.write(converter(match))
                    else:
                        if in_ordered_list:
                            html.write('</ol>\n')
                            in_ordered_list = False
                        if in_unordered_list:
                            html.write('</ul>\n')
                            in_unordered_list = False
                        html.write(converter(match))
                    matched = True
                    break

            if not matched:
                if in_ordered_list:
                    html.write('</ol>\n')
                    in_ordered_list = False
                if in_unordered_list:
                    html.write('</ul>\n')
                    in_unordered_list = False
                in_paragraph = True
                paragraph_lines.append(process_line(stripped_line))

        # Close any open lists or paragraphs at the end of the file
        if in_ordered_list:
            html.write('</ol>\n')
        if in_unordered_list:
            html.write('</ul>\n')
        if in_paragraph:
            html.write('<p>\n' + '<br/>\n'.join(paragraph_lines) + '\n</p>\n')


def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(input_file, output_file)
    sys.exit(0)


if __name__ == "__main__":
    main()
