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
        if "\n\n" in content:
            blocks = content.split("\n\n")
        else:
            blocks = content.split("\r\n")
        for b in blocks:
            lines = b.strip().split("\n")
            lastline = None
            for idx, line in enumerate(lines):
                line = line.strip()
                try:
                    message = lastline
                    lastline = line
                    if line.startswith("-->"):
                        (file_name, line, column) = line[4:].split(":")[0:3]
                    else:
                        continue
                except Exception as err :
                    continue
                err_msg = "\n".join(lines[(idx+2):])
                full_item =  {'file_name': append_prefix + file_name, 'line': line, 'column' : column, 'text': message }
                errors.append(full_item)
    return {"errors" : errors, "warnings": warnings}


class SolidityRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    SolidityRunner(sys.argv[1].split(' '), '0.0.0.0')
