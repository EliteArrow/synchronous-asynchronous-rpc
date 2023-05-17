import json
import socket
import sys
import threading

Sip = "127.0.0.1"
Sport = 8080
Sync = 0
Async = 1
Invoke = 1
res = 2

class AsyncComputataion:
    def __init__(self, function, args):
        self.function = function
        self.args = args
        self.rpc_type = Async
        self.computation_id = None
        self.result = None

    def invoke(self):
       
        request = {
            "function": self.function,
            "args": self.args,
            "rpc_type": self.rpc_type,
            "request_type": Invoke,
        }
        
        tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsock.connect((Sip, Sport))
        tsock.send(json.dumps(request).encode())
        response = tsock.recv(65536).decode()
        response = json.loads(response)
        tsock.close()

        if "error" in response:
            raise RuntimeError(response["error"])

        if "response_type" not in response:
            raise RuntimeError("No response from server")

        self.computation_id = response["token"]

    def get_result(self):
        request = {
            "rpc_type": self.rpc_type,
            "token": self.computation_id,
            "request_type": res,
        }
        tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsock.connect((Sip, Sport))
        tsock.send(json.dumps(request).encode())
        response = tsock.recv(65536).decode()
        response = json.loads(response)
        tsock.close()
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise ValueError("No response received from server")

        self.result = response["result"]
        return self.result
