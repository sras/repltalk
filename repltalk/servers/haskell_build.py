from repltalk import baserunner
from repltalk.servers import haskell
import sys
import os
import re
import json

class HaskellRunner(baserunner.BaseRunner):
    def process_output(self, content):
        return haskell.make_error_blocks(content)

def main():
    HaskellRunner(sys.argv[1].split(' '), '0.0.0.0')
