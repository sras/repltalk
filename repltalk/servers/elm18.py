from repltalk import baserunner
import sys
import os
import re
import json

def make_error_blocks(out):
    items = []
    for out_one in out.split('\n'):
        if len(out_one.strip()) == 0:
            continue;
        try:
            errors = json.loads(out_one)
            for error in errors:
                filename = os.path.abspath(error['file'])
                line = error['region']['start']['line']
                line_end = error['region']['end']['line']
                col = error['region']['start']['column']
                tag = error['tag']
                details = error['details']
                error_text = "{}\n    {}\n".format(tag, details.replace('\n', '\n    '))
                items.append({'file_name': filename, 'line': line, 'column' : col, 'text': error_text })
        except json.JSONDecodeError as e:
            print("Decoding failed" + str(e))
            print("'{}'".format(out_one))
            pass
    return {"errors" : items, "warnings": []}

def get_msg(x):
    if isinstance(x, str):
        return x
    else:
        return x['string']

class ElmRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    ElmRunner("elm", ["make", "--report", "json"] + sys.argv[1:], 'localhost')
