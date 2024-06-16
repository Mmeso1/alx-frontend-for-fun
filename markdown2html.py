#!/usr/bin/env python3

import sys
import os
import re

def convert_md_to_html(md_file, html_file):
    # Define the markdown syntaxes and their corresponding HTML conversion functions
    syntaxes = [
        (r'((?:#){1,6}) (.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>\n'),
        (r'\* (.*)', lambda m: f'<li>{m.group(1)}</li>\n'),  # Ordered list
        (r'- (.*)', lambda m: f'<li>{m.group(1)}</li>\n'),  # Unordered list
    ]

    with open(md_file, 'r') as md, open(html_file, 'w') as html:
        in_ordered_list = False
        in_unordered_list = False

        for line in md:
            line = line.strip()
            matched = False
            for regex, converter in syntaxes:
                match = re.match(regex, line)
                if match:
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
                html.write(line + '\n')

        # Close any open lists at the end of the file
        if in_ordered_list:
            html.write('</ol>\n')
        if in_unordered_list:
            html.write('</ul>\n')

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
