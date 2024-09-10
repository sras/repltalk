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


#content = '''{"file": "db.py", "line": 8, "column": 27, "message": "Syntax error in type annotation", "hint": "Suggestion: Use Tuple[T1, ..., Tn] instead of (T1, ..., Tn)", "code": "syntax", "severity": "error"}
#{"file": "db.py", "line": 13, "column": 32, "message": "Syntax error in type annotation", "hint": "Suggestion: Use Tuple[T1, ..., Tn] instead of (T1, ..., Tn)", "code": "syntax", "severity": "error"}
#{"file": "db.py", "line": 21, "column": 8, "message": "Name \"conn\" is not defined", "hint": null, "code": "name-defined", "severity": "error"}
#{"file": "gui.py", "line": 1, "column": 0, "message": "Module \"PyQt5\" has no attribute \"Qt\"", "hint": null, "code": "attr-defined", "severity": "error"}
#{"file": "gui.py", "line": 18, "column": 12, "message": "Name \"alert\" is not defined", "hint": null, "code": "name-defined", "severity": "error"}
#{"file": "gui.py", "line": 21, "column": 8, "message": "Name \"alert\" is not defined", "hint": null, "code": "name-defined", "severity": "error"}
#{"file": "main.py", "line": 1, "column": 0, "message": "Module \"PyQt5\" has no attribute \"Qt\"", "hint": null, "code": "attr-defined", "severity": "error"}
#'''

def make_error_blocks(content):
    errors = []
    warnings = []
    if content is not None and len(content) > 0:
        blocks = content.strip().split("\n")
        for l in blocks:
            b = json.loads(l)
            if b["hint"]:
                hint = b["hint"]
            else:
                hint = ""
            full_item = {'file_name': append_prefix + b["file"], 'line': b["line"], 'column' : b["column"], 'text': b["message"] + " " + hint  }
            if b["severity"] == "error":
                errors.append(full_item)
            else:
                warnings.append(full_item)
    return {"errors" : errors, "warnings": warnings}

def extract_filename(fn):
    fsi = fn.find('>')
    if fsi == -1:
        return fn
    else:
        return fn[(fsi+1):].strip()


class PythonRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    PythonRunner(sys.argv[1].split(' '), '0.0.0.0')
