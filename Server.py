from json import decoder, load
from socket import *
import time
import signal
import json


# Testing only, for Ctrl + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

QUERY_LISTDATA = "!SEND_LISTDATA"


ADDRESS = (gethostbyname(gethostname()), 39000)

s = socket(AF_INET, SOCK_DGRAM)

s.bind(ADDRESS)
print(f"[*] Socket at {ADDRESS[0]} at {ADDRESS[1]}")

# Test send the list of data
# Send ListData.json file in folder ServerFile

SERVER_DATA_FOLDER = "ServerFile"
SERVER_IMAGE_FOLDER = "Image Server"
SERVER_FILE_LISTDATA_NAME = "ListData.json"
fServerListData = open(f"{SERVER_DATA_FOLDER}/{SERVER_FILE_LISTDATA_NAME}", "rb")
jsonServerListData = json.loads(fServerListData.read().decode())

while True:
    data, addr = s.recvfrom(1024)
    print(f"[*] Receive {data.decode()} from address {addr[0]} at port {addr[1]}")

    if data.decode() == QUERY_LISTDATA:
        s.sendto(SERVER_FILE_LISTDATA_NAME.encode(), addr)
        print(
            f"[*] Send {SERVER_FILE_LISTDATA_NAME.encode()} to address {addr[0]} at port {addr[1]}"
        )

        while chunk := fServerListData.read(1024):
            s.sendto(chunk, addr)
            # print(f"Send to address {addr[0]} at port {addr[1]}")

        print(
            f"[*] Done send command {QUERY_LISTDATA} to address {addr[0]} at port {addr[1]}"
        )
    elif data.decode().find("SEND_IMAGE_AT_") != -1:
        # SEND_IMAGE_AT_1_0 -> ['SEND', 'IMAGE', 'AT', '1', '0']

        command = data.decode()
        IndexListData = int(command.split("_")[3])
        IndexImageData = int(command.split("_")[4])

        NameImage = jsonServerListData[IndexListData - 1].get("image")[IndexImageData]

        with open(
            f"{SERVER_DATA_FOLDER}/{SERVER_IMAGE_FOLDER}/{NameImage}", "rb"
        ) as fImage:
            s.sendto(NameImage.encode(), addr)
            print(
                f"[*] Send {NameImage.encode()} to address {addr[0]} at port {addr[1]}"
            )

            while chunk := fImage.read(1024):
                s.sendto(chunk, addr)
                # print(f"Send to address {addr[0]} at port {addr[1]}")

        print("[*] Done")
