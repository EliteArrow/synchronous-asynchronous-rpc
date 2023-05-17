import time

from client import AsyncComputataion

def main():
    print("\n waiting..\n")
    time.sleep(2)
    print("Requesting to add(1, 2)")
    add_rpc = AsyncComputataion("add", args=[1, 2])
    add_rpc.invoke()
    print("Results = {}".format(add_rpc.get_result()))

    print("\n waiting..\n")
    time.sleep(2)
    print("Requesting to sort[51,13,32,23,4,3,1]")
    array= [51,13,32,23,4,3,1]
    sortRpc = AsyncComputataion("sort", args=[array])
    sortRpc.invoke()
    print("Results = {}".format(sortRpc.get_result()))
  

if __name__ == "__main__":
    main()
