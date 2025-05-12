from repltalk import baserunner
import sys
import os
import re
import json

try:
    append_prefix = os.environ['REPLTALK_APPEND_PREFIX']
    print("{}={}".format("REPLTALK_APPEND_PREFIX", append_prefix));
except:
    append_prefix = ''

def make_error_blocks(content):
    errors = []
    warnings = []
    if content is not None and len(content) > 0:
        lines = content.split("\n")
        for idx, line in enumerate(lines):
            try:
                print(line.split(": ")[0:2])
                (file_name, line, column, type_, msg) = line.split(":")[0:5]
            except Exception as err :
                continue
            type_ = type_.strip()
            full_item =  {'file_name': append_prefix + file_name, 'line': line, 'column' : column, 'text': msg }
            if "error" in type_:
                errors.append(full_item)
            elif "warning" in type_:
                warnings.append(full_item)
    return {"errors" : errors, "warnings": warnings}

class CRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    CRunner(sys.argv[1].split(' '), '0.0.0.0')
