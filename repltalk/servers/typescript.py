from repltalk import baserunner
import sys
import os
import re
import json

try:
    append_prefix = os.environ['REPLTALK_APPEND_PREFIX']
except:
    append_prefix = ''

def extract_filename(flc):
    opening = flc.index("(")
    file_name = flc[0:opening]
    (l, c) = flc[opening+1 : -1].split(',')
    return (file_name, l, c)

def make_error_blocks(content):
    print(content)
    errors = []
    warnings = []
    if content is not None and len(content) > 0:
        if "\n" in content:
            lines = content.split("\n")
        else:
            lines = content.split("\r\n")
        for idx, line in enumerate(lines):
            try:
                segments = line.split(":")
                (file_name_lc, type_) = segments[0:2]
                (file_name, line, column) = extract_filename(file_name_lc)
            except Exception as err :
                continue
            type_ = type_.strip()
            full_item =  {'file_name': append_prefix + file_name.strip(), 'line': line, 'column' : column, 'text': ''.join(segments[2:]).strip() + "\n" + collect_err_lines(lines, idx) }
            if "error" in type_:
                errors.append(full_item)
            elif "warning" in type_:
                warnings.append(full_item)
    return {"errors" : errors, "warnings": warnings}

def collect_err_lines(lines, start_idx):
    ret = []
    idx = start_idx
    leng = len(lines)
    while True:
        idx = idx + 1
        if (idx > leng - 1) or lines[idx].startswith("  "):
            ret.append(lines[idx])
        else:
            return '\n'.join(ret)

class TypescriptRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    TypescriptRunner(sys.argv[1].split(' '), '0.0.0.0')
