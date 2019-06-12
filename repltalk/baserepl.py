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
    NOT_STARTED = 0
    KILLED = 0
    WAITING_COMMAND = 1
    RUNNING = 2

class BaseRepl:
    def __init__(self, prompt, cmd, args, host):
        self.process = None
        self.status = Status.NOT_STARTED

        port = getport()

        @route('/start')
        def start_handler():
            if self.status == Status.NOT_STARTED:
                threading.Thread(target=self.thread_callback, args=(prompt, cmd, args), daemon=True).start()
                time.sleep(1)
                self.expect(prompt)
                self.status = Status.WAITING_COMMAND
                return command_response(self.get_output())
            else:
                return command_error("CANNOT_RESTART")

        @route('/stop')
        def stop_handler():
            self.process.terminate(force=True)
            self.status = Status.KILLED

        @route('/command', method='POST')
        def command_handler():
            command = request.json['command']
            if self.status == Status.WAITING_COMMAND:
                self.process.sendline(command)
                self.status = Status.RUNNING
                self.expect(prompt)
                self.status = Status.WAITING_COMMAND
                return command_response(self.get_output())
            elif self.status == Status.NOT_STARTED:
                return command_error('NOT_STARTED')
        run(host=host, port=getport())

    def get_output(self):
        return self.process_output(self.process.before.replace('\r\n', '\n'))

    def process_output(self, content):
        raise NotImplementedError("Please Implement this method in sub class")

    def expect(self, prompt):
        self.process.expect_exact([prompt], timeout=None)

    def thread_callback(self, prompt, cmd, args):
        print("Starting REPL process with command: {}".format(' '.join([cmd] + args)))
        self.process = pexpect.spawn(cmd, args, encoding=sys.stdout.encoding)
        self.process.logfile_read = sys.stdout # Set this to 'sys.stdout' to enable logging...
        outlines = []
