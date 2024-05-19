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


# Compiling using func v0.4.4
# contracts/my_contract.fc:26:25: error: undefined function `ctx_idd`, defining a global function of unknown type
#               .store_uint(ctx_idd, 32)
#                           ^
# Func compilation error: contracts/my_contract.fc:27:13: error: cannot apply function store_uint : (builder, int, int) -> builder to arguments of type (builder, ??11 -
# > ??12, int): cannot unify type ??11 -> ??12 with int
#               .store_uint(ctx_counter, 32)

def make_error_blocks(content):
    errors = []
    warnings = []
    if content is not None and len(content) > 0:
        lines = content.strip().split("\n")
        print(lines)
        for idx, line in enumerate(lines):
            print("line = {}".format(line))
            try:
                (file_name, line_no, column, err_type, err_msg) = line.split(":")[0:5]
                if file_name == "Func compilation error":
                    (_, file_name, line_no, column, err_type, err_msg) = line.split(":")[0:6]
            except Exception as err :
                print(err)
                continue
            full_item =  {'file_name': append_prefix + file_name.strip(), 'line': line_no, 'column' : column, 'text': err_type + "\n" + err_msg.strip() }
            errors.append(full_item)
    print(errors)
    return {"errors" : errors, "warnings": warnings}

class FunCRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return make_error_blocks(content)

def main():
    FunCRunner(sys.argv[1].split(' '), '0.0.0.0')
