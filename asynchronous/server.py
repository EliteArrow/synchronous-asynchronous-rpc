import json
import socket
import random

Sip = "127.0.0.1"
Sport = 8080
Sync = 0
Async = 1
Invoke = 1
ReqR = 2
Ack = 1
ResR = 2
Reults = dict()

def generataError(con, msg):
    reply = json.dumps({"error": msg})
    con.send(reply.encode())

def add(x, y):
    return x + y

def sort(array):
    return sorted(array)

def process_async_rpc(con, request):
    if request["request_type"] == Invoke:
        token = random.randint(1, 10000)
        f = globals().get(request["function"])
        if not f:
            generataError(con, "invalid function")
            return
        reply = json.dumps({"response_type": Ack, "token": token})
        con.send(reply.encode())
        try:
            result = f(*request["args"])
            Reults[token] = result
        except Exception:
            generataError(con, "error while execution")
    elif request["request_type"] == ReqR:
        token = int(request["token"])
        result = Reults[token]
        reply = json.dumps({"result": result, "response_type": ResR})
        con.send(reply.encode())
    else:
        generataError(con, "invalid request")

def main():
    tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsock.bind((Sip, Sport))
    tsock.listen(5)
    while True:
        con, _sender_address = tsock.accept()
        request = json.loads(con.recv(65536).decode())
        process_async_rpc(con, request)
        con.close()

if __name__ == "__main__":
    main()
