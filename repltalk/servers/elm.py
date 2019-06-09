from repltalk import baserunner
import sys
import os
import re
import json

def make_error_blocks(content):
    print(content)
    if len(content) == 0:
        return {"errors" : [], "warnings": []}
    else:
        try:
            items = []
            errors = json.loads(content)
            for error in errors['errors']:
                for problem in error['problems']:
                    filename = os.path.abspath(error['path'])
                    line = problem['region']['start']['line']
                    line_end = problem['region']['end']['line']
                    col = problem['region']['start']['column']
                    tag = problem['title']
                    details =  ''.join([get_msg(x) for x in problem['message'] ])
                    items.append({'file_name': filename, 'line': line, 'column' : col, 'text': "{}\n{}".format(tag, details) })
            return {"errors" : items, "warnings": []}
        except json.JSONDecodeError as e:
            print("Decoding failed" + str(e) + content)
            pass

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
