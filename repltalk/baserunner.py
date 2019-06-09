import subprocess
import io
import sys
import time
import threading
import sys
import pipes
import os
import pexpect
import pexpect.exceptions
import json
from bottle import route, run, request
from enum import Enum

def command_response(o):
    return json.dumps({'output': o})

def command_error(e):
    return json.dumps({'error': e})

def getport():
    try:
        return int(os.environ['LANGUAGE_SERVER_PORT'])
    except:
        return 2096

class Status(Enum):
    WAITING_COMMAND = 1
    RUNNING = 2

class BaseRunner:
    def __init__(self, cmd, args, host):

        port = getport()
        self.status = Status.WAITING_COMMAND

        @route('/start')
        def start_handler():
            return command_response("")

        @route('/stop')
        def stop_handler():
            return command_response("")

        @route('/command', method='POST')
        def run_handler():
            if self.status == Status.WAITING_COMMAND:
                self.status = Status.RUNNING
                result = subprocess.run([cmd]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                error_ = result.stderr.decode()
                output_ = result.stdout.decode()
                self.status = Status.WAITING_COMMAND
                if len(error_) > 0:
                    return command_response(self.process_output(error_))
                else:
                    return command_response(self.process_output(output_))
            else:
                return command_error("Already started")
        run(host=host, port=getport())

    def process_output(self, content):
        raise NotImplementedError("Please Implement this method in sub class")
