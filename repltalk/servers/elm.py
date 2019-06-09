from repltalk import baserunner
import sys
import os
import re
import json

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

class FileMarker:
    def __init__(self):
        self.buffer = {}

    def get_region(self, file_name, line_start, line_end):
        line_start -= 1
        try:
            fcontent = self.buffer[file_name]
        except KeyError:
            with open(file_name, 'r') as fin:
                fcontent = fin.readlines()
                self.buffer[file_name] = fcontent

        return ''.join(["   > {}: {}".format(y+1,x) for (x, y) in zip(fcontent[line_start:line_end], range(line_start, line_end)) ])

def make_error_blocks(content):
    print(content)
    if len(content) == 0:
        return {"errors" : [], "warnings": []}
    else:
        fm = FileMarker();
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
