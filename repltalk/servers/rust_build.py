from repltalk import baserunner
import sys
import os
import re
import json

try:
    append_prefix = os.environ['REPLTALK_APPEND_PREFIX']
except:
    append_prefix = ''

def make_error_blocks(content):
    errors = []
    warnings = []
    if content is not None and len(content) > 0:
        if "\n\n" in content:
            blocks = content.split("\n\n")
        else:
            blocks = content.split("\r\n")
        for b in blocks:
            lines = b.strip().split("\n")
            for idx, line in enumerate(lines):
                try:
                    print(line.split(":")[0:2])
                    (type_, msg) = line.split(":")[0:2]
                    (_, file_loc) = lines[idx+1].split("-->")
                    (file_name, line, column) = file_loc.strip().split(":")
                except Exception as err :
                    continue
                type_ = type_.strip()
                err_msg = "\n".join(lines[(idx+2):])
                full_item =  {'file_name': append_prefix + file_name, 'line': line, 'column' : column, 'text': msg + "\n" + err_msg.strip() }
                if "error" in type_:
                    errors.append(full_item)
                elif "warning" in type_:
                    warnings.append(full_item)
    return {"errors" : errors, "warnings": warnings}

def extract_filename(fn):
    fsi = fn.find('>')
    if fsi == -1:
        return fn
    else:
        return fn[(fsi+1):].strip()


class RustRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    RustRunner(sys.argv[1].split(' '), 'localhost')
