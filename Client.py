from os import path
from socket import *
import time
import signal
import json
from tkinter import *
from PIL import ImageTk, Image

# Testing only, for Ctrl + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

CLIENT_TMP_FOLDER = "ClientTmp"
SERVER_FILE_LISTDATA_NAME = "ListData.json"

QUERY_LISTDATA = "!SEND_LISTDATA"
QUERY_IMAGE = "!SEND_IMAGE_AT_"

s = socket(AF_INET, SOCK_DGRAM)
SERVER_ADDRESS_PORT = ("192.168.1.10", 39000)


# s.sendto(QUERY_LISTDATA.encode(), SERVER_ADDRESS_PORT)
# print(f"Send to address {SERVER_ADDRESS_PORT[0]} at port {SERVER_ADDRESS_PORT[1]}")

# data, addr = s.recvfrom(2048)
# print(f"Receive from address {addr[0]} at port {addr[1]}")

# fClientListData = open(f"{CLIENT_TMP_FOLDER}/{SERVER_FILE_LISTDATA_NAME}", "wb")
# try:
#     while dataAddr := s.recvfrom(2048):
#         fClientListData.write(dataAddr[0])

#         print(f"Receive from address {dataAddr[1][0]} at port {dataAddr[1][1]}")
#         s.settimeout(0.5)
# except timeout:
#     fClientListData.close()

# print("## DONE")

root = Tk()

# List chứa các ImageTk
# Nếu mà load xong ra khỏi loop thì hình sẽ lên hình gì cả
imageFile = []

with open("ClientTmp/ListData.json", "rb") as f:
    data = f.read().decode("utf-8")
    my_json = json.loads(data)
    for j in range(0, len(my_json[5].get("image"))):
        isImageLoad = False

        while isImageLoad == False:
            command = QUERY_IMAGE + str(5) + "_" + str(j)
            s.sendto(command.encode(), SERVER_ADDRESS_PORT)

            print(
                f"[*] Send {command} to address {SERVER_ADDRESS_PORT[0]} at port {SERVER_ADDRESS_PORT[1]}"
            )

            data, addr = s.recvfrom(1024)
            print(f"[*] Receive from address {addr[0]} at port {addr[1]}")

            pathImage = f"{CLIENT_TMP_FOLDER}/{data.decode()}"

            fImageData = open(pathImage, "wb")
            try:
                while dataAddr := s.recvfrom(1024):
                    fImageData.write(dataAddr[0])
                    # print(
                    #     f"Receive from address {dataAddr[1][0]} at port {dataAddr[1][1]}"
                    # )

                    s.settimeout(0.1)
            except timeout:
                fImageData.close()
                print(f"[*] Done {command}")

            try:
                imageFile.append(
                    ImageTk.PhotoImage(
                        Image.open(pathImage).resize((100, 100), Image.ANTIALIAS)
                    )
                )

                print(f"[*] The {pathImage} has loaded")
                isImageLoad = True

            except Exception as exception:
                print(f"[!] {exception}")

for mem in imageFile:
    lbl = Label(root, image=mem)
    lbl.pack()

root.mainloop()

print("[*] Done")


# print(f"[*] The {pathImage} is loaded done")
# isImageLoaded = True

# root = Tk()
# # width x height
# root.geometry("500x200")

# titleLbl = Label(root, text="Địa điểm yêu thích")
# titleLbl.pack()

# dcrpLbl = Label(root, text="Click chuột để chọn địa điểm", height=30)
# dcrpLbl.pack()

# lb = Listbox(root)
# lb.insert

# lb.pack()

# root.mainloop()
