import json
import socket


IP = socket.gethostbyname(socket.gethostname())
PORT = 6060

def send_error(con, msg):
    reply = json.dumps({"error": msg})
    con.send(reply.encode())

def add(x, y):
    return x + y

def sort(array):
    return f"Sorted Array : {sorted(array)}"

def rpc(con, request):
    request = json.loads(request)
    f = globals().get(request["fn"])
    if not f:
        send_error(con, "invalid function")
        return
    try:
        result = f(*request["args"])
        reply = json.dumps({"result": result})
        con.send(reply.encode())
    except Exception:
        send_error(con, "error")


def main():
    tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsock.bind((IP, PORT))
    tsock.listen(5)
    while True:
        con, _sender_address = tsock.accept()
        request = con.recv(65536).decode()
        rpc(con, request)
        con.close()


if __name__ == "__main__":
    main()