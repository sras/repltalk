from repltalk import baserepl
import tempfile
import sys
import os
import re

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def make_error_blocks(content):
    content = ansi_escape.sub('', content)
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
                    (file_name, line, column, type_, msg) = line.split(":")[0:5]
                except Exception as err :
                    continue
                type_ = type_.strip()
                err_msg = "\n".join(lines[idx:])
                full_item =  {'file_name': file_name, 'line': line, 'column' : column, 'text': err_msg }
                if "error" in type_:
                    errors.append(full_item)
                elif "warning" in type_:
                    warnings.append(full_item)
    return {"errors" : errors, "warnings": warnings}


class GHCIRepl(baserepl.BaseRepl):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    prompt = 'REPLTALKPROMPT>>>'
    (f, fname) = tempfile.mkstemp()
    fo = os.fdopen(f, mode='w')
    fo.write(":set prompt {}".format(prompt))
    fo.close()
    GHCIRepl(prompt, "stack", ["ghci", "--ghci-options=-ghci-script={}".format(fname)] + sys.argv[1:], 'localhost')
