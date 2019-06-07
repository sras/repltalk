from repltalk import baseadapter
import sys
import os
import socket
import threading
import time
import json

def build_error_list(items, file_map=None):
    ret = []
    for (idx, e) in enumerate(items['errors']):
        for (idx1, ln) in enumerate(e['text'].split('\n')):
            # We attach each line to the error, keeping the error no (nr) same for the
            # lines belonging to same error.
            if idx1 == 0:
                ret.append({'filename': apply_file_map(e['file_name'], file_map), 'lnum': e['line'], 'col': e['column'], 'text': ln, 'nr': idx, 'type': 'E'})
            else:
                ret.append({'text': ln, 'nr': idx, 'type': 'E'})

    for (idx, e) in enumerate(items['warnings']):
        for (idx1, ln) in enumerate(e['text'].split('\n')):
            if idx1 == 0:
                ret.append({'filename': apply_file_map(e['file_name'], file_map), 'lnum': e['line'], 'col': e['column'], 'text': ln, 'nr': idx, 'type': 'W'})
            else:
                ret.append({'text': ln, 'nr': idx, 'type': 'W'})
    return ret

def apply_file_map(path, file_map):
    if file_map is not None:
        for fromp in file_map:
            if path.startswith(fromp):
                return "{}{}".format(file_map[fromp], path[len(fromp):])
        return path
    else:
        return path


def get_file_mapping():
    try:
        file_mapping = sys.argv[1]
        parts = file_mapping.split(':')
        if len(parts) == 2:
            return {parts[0] : parts[1]}
    except IndexError:
        return None

def get_vim_address():
    return os.environ['VIM_SERVERNAME']

class VIM(baseadapter.BaseAdapter):
    def __init__(self):
        self.connected_socket = None
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('127.0.0.1', 0))
        port = serversocket.getsockname()[1]
        def thread_callback(socket):
            serversocket.listen(1)
            while True:
                (clientsocket, _) = serversocket.accept()
                self.connected_socket = clientsocket
                print("Connected to vim instance from socket : {}".format(self.connected_socket.getsockname()[1]))
                break
        threading.Thread(target=thread_callback, args=[serversocket], daemon=True).start()
        vim_server = get_vim_address()
        while not self.connected_socket:
            print("Waiting for connection from vim")
            cmd = "vim --servername {} --remote-expr \"execute('let chan = ch_open(\\\"localhost:{}\\\", {{\\\"mode\\\":\\\"json\\\"}})')\"".format(vim_server, port)
            print(cmd)
            os.system(cmd)
            time.sleep(0.2)
        super().__init__()

    def call_vim_function(self, func, args):
        self.connected_socket.sendall(json.dumps(["call", func, args]).encode('utf-8'))
        self.connected_socket.sendall(json.dumps(["redraw", ""]).encode('utf-8'))

    def show_activity(self):
        self.call_vim_function('REPLTalkIndicateActivity', [])

    def send_result(self, msg):
        print("Neovim send result")
        try:
            elist = build_error_list(msg['output'], get_file_mapping())
            if len(msg['output']['errors']) > 0:
                self.call_vim_function('REPLTalkIndicateError', [])
            elif len(msg['output']['warnings']) > 0:
                self.call_vim_function('REPLTalkIndicateWarnings', [])
            else:
                self.call_vim_function('REPLTalkIndicateSuccess', [])
            self.call_vim_function('setqflist', [[], 'r', {"items": elist, "title": "REPLTalk Error list"}])
        except Exception as e:
            print("Caught exception {}".format(e))
            pass

def main():
    VIM()
