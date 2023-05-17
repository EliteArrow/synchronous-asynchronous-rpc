import json
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 6060

def rpc(fn, args):    
    request = {"fn": fn, "args": args}
    tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsock.connect((IP, PORT))
    tsock.send(json.dumps(request).encode())
    response = tsock.recv(65536).decode()
    tsock.close()
    response = json.loads(response)
    if "error" in response:
        raise RuntimeError(response["error"])
    return response["result"]

def main():
 firstNum = int(input("Enter first number"))
 secontNum = int(input("Enter second number"))
 print(rpc("add", args=[firstNum,secontNum]))

 num = int(input("Enter the size of the Array"))
 if(num >0):
    arr = []
    for i in range(num):
        arr.append(int(input(f"Enter {i} element")))
    print(f"Input Array : {arr}")
    print(rpc("sort", args=[arr]))
 else:
    print("Invalid Input:")

if __name__ == "__main__":
    main()