from bottle import route, run, request
import json
import http.client
import os
import time

def getport():
    try:
        return int(os.environ['ADAPTER_PORT'])
    except:
        return 2097

def getreplport():
    try:
        return int(os.environ['LANGUAGE_SERVER_PORT'])
    except:
        return 2096

class BaseAdapter():
    def __init__(self):
        self.repl_port = getreplport()
        start_output = self.repl_start()
        self.send_result(start_output)

        @route('/start')
        def start_handler():
            start_output = self.start_repl()
            self.send_result(start_output)

        @route('/stop')
        def stop_handler():
            self.stop_repl()

        @route('/command', method='POST')
        def command_handler():
            command = request.json['command']
            self.show_activity()
            command_output = self.repl_command(command)
            self.send_result(command_output)
        run(host='localhost', port=getport())

    def send_req(self, path, data = False):
        while True:
            try:
                conn = http.client.HTTPConnection("localhost:{}".format(self.repl_port))
                if data:
                    print("Sending data {}".format(data))
                    conn.request("POST", path, json.dumps(data), headers = {'Content-type': 'application/json'})
                else:
                    conn.request("GET", path)
                break
            except:
                print("Connection error, retrying after 1 sec")
                time.sleep(1)
                pass
        res = conn.getresponse()
        return res.read()

    def repl_start(self):
        return self.send_req("/start")

    def repl_command(self, command):
        return json.loads(self.send_req("/command", {'command': command}))

    def repl_stop(self):
        return self.send_req("/stop")

    def show_activity(self):
        raise NotImplementedError("Please Implement this method in sub class")

    def send_result(self, result):
        raise NotImplementedError("Please Implement this method in sub class")
