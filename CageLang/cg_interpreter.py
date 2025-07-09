#!/usr/bin/env python

import sys
import re

SYNTAX_RULES = {
    "cycle True": ["while True", 0],
    "log": ["print", 1],
}

COMMENT_SYMBOL = "//"
MULTILINE_COMMENT_SYMBOLS = ["/*", "*/"]
INVALID_COMMENT_SYMBOLS = ["#", "--", "::", "||"]
INVALID_MULTILINE_SYMBOLS = ["(*", "*)", "[*", "*]", "{*", "*}"]

def translate_code(cage_code_lines):
    translated_lines = []
    sorted_rules = sorted(SYNTAX_RULES.items(), key=lambda item: len(item[0]), reverse=True)

    escaped_comment_symbol = re.escape(COMMENT_SYMBOL)
    comment_pattern = re.compile(r'^(.*?)\s*(' + escaped_comment_symbol + r'.*)$')
    python_comment_pattern = re.compile(r'^(.*?)\s*(#.*)$')

    multiline_comment_open = False
    multiline_buffer = []

    for line_num, line in enumerate(cage_code_lines, 1):
        current_line = line.rstrip('\n')
        
        if not current_line.strip():
            translated_lines.append(current_line)
            continue

        if multiline_comment_open:
            if MULTILINE_COMMENT_SYMBOLS[1] in current_line:
                multiline_comment_open = False
                multiline_buffer.append(current_line.split(MULTILINE_COMMENT_SYMBOLS[1])[0])
                translated_lines.append("#" + "\n#".join(multiline_buffer))
                translated_lines.append(current_line.split(MULTILINE_COMMENT_SYMBOLS[1])[1])
                multiline_buffer = []
            else:
                multiline_buffer.append(current_line)
            continue

        for invalid_symbol in INVALID_MULTILINE_SYMBOLS[::2]:
            if invalid_symbol in current_line:
                sys.stderr.write(f"Error: Invalid multiline comment symbol '{invalid_symbol}'\n")
                sys.exit(1)

        if MULTILINE_COMMENT_SYMBOLS[0] in current_line:
            if MULTILINE_COMMENT_SYMBOLS[1] in current_line:
                parts = current_line.split(MULTILINE_COMMENT_SYMBOLS[1])
                translated_lines.append("#" + parts[0].split(MULTILINE_COMMENT_SYMBOLS[0])[1] + parts[1])
            else:
                multiline_comment_open = True
                multiline_buffer.append(current_line.split(MULTILINE_COMMENT_SYMBOLS[0])[1])
            continue

        our_comment_match = comment_pattern.match(current_line)
        python_comment_match = python_comment_pattern.match(current_line)

        if our_comment_match:
            code_part = our_comment_match.group(1)
            comment_part = our_comment_match.group(2)

            for invalid_symbol in INVALID_COMMENT_SYMBOLS:
                if invalid_symbol in code_part:
                    sys.stderr.write(f"Error: Invalid comment symbol '{invalid_symbol}'\n")
                    sys.exit(1)
            
            translated_comment_part = "#" + comment_part[len(COMMENT_SYMBOL):]
            current_line = code_part + translated_comment_part
            
        elif python_comment_match:
            sys.stderr.write(f"Error: Use '{COMMENT_SYMBOL}' for comments, not '#'\n")
            sys.exit(1)
        
        modified_line = current_line.strip()

        for cage_syntax, (python_syntax, exclusive_flag) in sorted_rules:
            if exclusive_flag == 1:
                pattern = r'\b' + re.escape(python_syntax) + r'\b'
                if re.search(pattern, modified_line):
                    is_part_of_cage_syntax = False
                    for cs, _ in sorted_rules:
                        if python_syntax in cs and cage_syntax != python_syntax: 
                            is_part_of_cage_syntax = True
                            break
                    if not is_part_of_cage_syntax:
                        sys.exit(1)

        for cage_syntax, (python_syntax, _) in sorted_rules:
            pattern = r'\b' + re.escape(cage_syntax) + r'\b'
            current_line = re.sub(pattern, python_syntax, current_line)
        
        translated_lines.append(current_line)
    
    return "\n".join(translated_lines)

def run_cage_interpreter(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            cage_code = f.readlines()
    except FileNotFoundError:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

    python_code = translate_code(cage_code)
    
    try:
        exec(python_code)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    cage_file = sys.argv[1]
    run_cage_interpreter(cage_file)
