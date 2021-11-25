from concurrent.futures import thread
from socket import *
import threading
import json

from tkinter import *
from tkinter import messagebox

import signal

# Testing only, for Ctrl + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Constant value

# Message between server and client
START_CONNET = "!SOCKET_CONNECT"
REPLY_START_CONNECT = "!CONNECT_CREATE"
QUERY_LISTDATA = "!SEND_LISTDATA"
QUERY_IMAGE_prefix = "!SEND_IMAGE_AT_"
TERMINATE_CONNET = "!SOCKET_TERMINATE"

# Name of file and folder
SERVER_DATA_FOLDER = "ServerFile"
SERVER_IMAGE_FOLDER = "Image Server"
SERVER_FILE_LISTDATA_NAME = "ListData.json"

# Global variable
isSocketRunning = False


def loopSocketListen(sck):
    while isSocketRunning == True:
        data, addr = sck.recvfrom(1024)
        print(f"[*] Receive {data.decode()} from address {addr[0]} at port {addr[1]}")

        # !SOCKET_CONNECT
        if data.decode() == START_CONNET:
            sck.sendto(REPLY_START_CONNECT.encode(), addr)
            print(
                f"[-] Send {REPLY_START_CONNECT} to address {addr[0]} at port {addr[1]}"
            )

        # !SEND_LISTDATA
        elif data.decode() == QUERY_LISTDATA:
            sck.sendto(SERVER_FILE_LISTDATA_NAME.encode(), addr)
            print(
                f"[-] Send {SERVER_FILE_LISTDATA_NAME.encode()} to address {addr[0]} at port {addr[1]}"
            )

            fServerListData = open(
                f"{SERVER_DATA_FOLDER}/{SERVER_FILE_LISTDATA_NAME}", "rb"
            )

            while chunk := fServerListData.read(1024):
                sck.sendto(chunk, addr)
                # print(f"Send to address {addr[0]} at port {addr[1]}")

            print(
                f"[!] Done send command {QUERY_LISTDATA} to address {addr[0]} at port {addr[1]}"
            )

        # SEND_IMAGE_AT_X_Y where X = code and Y = index of image
        elif data.decode().startswith(QUERY_IMAGE_prefix) == True:
            # SEND_IMAGE_AT_1_0 -> ['SEND', 'IMAGE', 'AT', '1', '0']
            command = data.decode()
            IndexListData = int(command.split("_")[3])
            IndexImageData = int(command.split("_")[4])

            fServerListData = open(
                f"{SERVER_DATA_FOLDER}/{SERVER_FILE_LISTDATA_NAME}", "rb"
            )
            jsonServerListData = json.loads(fServerListData.read().decode())

            NameImage = jsonServerListData[IndexListData - 1].get("image")[
                IndexImageData
            ]

            with open(
                f"{SERVER_DATA_FOLDER}/{SERVER_IMAGE_FOLDER}/{NameImage}", "rb"
            ) as fImage:
                sck.sendto(NameImage.encode(), addr)
                print(
                    f"[-] Send {NameImage.encode()} to address {addr[0]} at port {addr[1]}"
                )

                while chunk := fImage.read(1024):
                    sck.sendto(chunk, addr)
                    # print(f"Send to address {addr[0]} at port {addr[1]}")

            print(f"[!] Done send {NameImage} to address {addr[0]} at port {addr[1]}")

        elif data.decode() == TERMINATE_CONNET:
            print(f"[!] Socket is terminate")


def handle_BtnClick():
    global isSocketRunning

    if isSocketRunning == False:
        global sck
        global tAddrPort

        isSocketRunning = True

        tAddrPort = (gethostbyname(gethostname()), 39000)

        sck = socket(AF_INET, SOCK_DGRAM)
        sck.bind(tAddrPort)
        print(f"[!] Socket at {tAddrPort[0]} at {tAddrPort[1]}")

        global thdSocketListen
        thdSocketListen = threading.Thread(target=loopSocketListen, args=[sck])
        thdSocketListen.start()

        global statusLbl

        statusLbl = Label(
            root,
            text=f"The socket is on address {tAddrPort[0]}:{tAddrPort[1]}",
            fg="green",
            bd=1,
            relief=SUNKEN,
            anchor=E,
        ).grid(row=2, column=0, columnspan=2, sticky=W + E)

    else:
        messagebox.showerror("Error!!", "The socket already haved create")


# Exit button on window, upper right conner of window
def handle_BtnExit(tkWindow):
    global isSocketRunning

    if isSocketRunning == True:
        if messagebox.askokcancel("Quit", "Do you want turn off server?"):
            tkWindow.destroy()

            isSocketRunning = False
            sck.sendto(TERMINATE_CONNET.encode(), tAddrPort)
            thdSocketListen.join()
            exit
    else:
        if messagebox.askokcancel("Quit", "Do you want turn off server?"):
            tkWindow.destroy()
            exit


def main():
    global root
    global btn
    global statusLbl

    root = Tk()
    root.title("Server")
    # root.geometry("240x160")
    root.resizable(False, False)

    btn = Button(
        root,
        text="Press to start server",
        padx=50,
        pady=50,
        command=lambda: handle_BtnClick(),
    ).grid(row=0, column=0, padx=20, pady=20)

    statusLbl = Label(
        root, text="Press button to start server", bd=1, relief=SUNKEN, anchor=E
    ).grid(row=2, column=0, columnspan=2, sticky=W + E)

    root.protocol("WM_DELETE_WINDOW", lambda: handle_BtnExit(root))
    root.mainloop()


main()
