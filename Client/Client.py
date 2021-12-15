import os
import signal
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from socket import *
import tkinter
from tkinter.ttk import Treeview
import ipaddress
from ClinentHelper import *

from PIL import ImageTk, Image

# Testing only, for Ctrl + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

CLIENT_TMP_FOLDER = "ClientTmp"
SERVER_FILE_LISTDATA_NAME = "ListData.json"

START_CONNET = "!SOCKET_CONNECT"
REPLY_START_CONNECT = "!CONNECT_CREATE"
QUERY_LISTDATA = "!SEND_LISTDATA"
QUERY_IMAGE_prefix = "!SEND_IMAGE_AT_"
TERMINATE_CONNET = "!SOCKET_TERMINATE"

# Check if ClientTmp folder is exist
# If not then create folder
isPathExsit = os.path.exists(f"./{CLIENT_TMP_FOLDER}")
if isPathExsit != True:
    os.mkdir(CLIENT_TMP_FOLDER)


class FirstScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("640x480")
        self.title("Local IP")
        self.resizable(False, False)

        # Frame
        self.mainFrame = tk.Frame(self, bg="blue")
        self.mainFrame.pack(fill="both", expand=True)

        # ICON
        appIcon = Image.open("ClientMaterial/ip.png")
        appIcon = ImageTk.PhotoImage(appIcon)
        self.iconphoto(False, appIcon)

        # BACKGROUND
        appBackground = Image.open("ClientMaterial/backgroundFirstWindow.jpg")
        appBackground = appBackground.resize((640, 480), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(appBackground)
        tk.Label(self.mainFrame, image=self.background).place(x=0, y=0)

        # IPLabel
        tk.Label(
            self.mainFrame,
            text="IP",
            font=("Goudy old style", 15, "bold"),
            fg="#000",
            bg="#FAFAFA",
        ).place(x=90, y=180)

        # IPEntry
        self.IPEntry = tk.Entry(
            self.mainFrame, font=("Goudy old style", 15), bg="#ECECEC"
        )
        self.IPEntry.place(x=150, y=180, width=350, height=35)

        # IPButton Submit
        tk.Button(
            self.mainFrame,
            command=self.submitIP,
            cursor="hand2",
            text="SUBMIT",
            fg="white",
            bg="#d77337",
            font=("Goudy old style", 20, "bold"),
        ).place(x=230, y=300, width=180, height=40)

        self.mainloop()

    def submitIP(self):
        try:
            # Try check if it is valid ip address
            HOST = ipaddress.ip_address(self.IPEntry.get())
            PORT = 39000

            s = socket(AF_INET, SOCK_DGRAM)

            global SERVER_ADDRESS_PORT
            SERVER_ADDRESS_PORT = (str(HOST), PORT)

            try:
                s.sendto(START_CONNET.encode(), SERVER_ADDRESS_PORT)
                s.settimeout(0.1)

                print(
                    f"[*] Send {START_CONNET} to address {SERVER_ADDRESS_PORT[0]} at port {SERVER_ADDRESS_PORT[1]}"
                )

                data, Addr_Port = s.recvfrom(1024)
                print(
                    f"[*] Receive {data.decode()} from address {Addr_Port[0]} at port {Addr_Port[1]}"
                )

                self.destroy()
                ClientScreen()

            except timeout:
                messagebox.showerror(
                    "No server", f"Cannot found server at ip {SERVER_ADDRESS_PORT[0]}"
                )

        except ValueError:
            messagebox.showerror(
                "Invaild Value", "The IP Address is not valid, please reinput"
            )


class ClientScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        # Must down list data
        self.downListData()

        self.title("List Address")
        self.geometry("800x330")
        self.resizable(False, False)

        self.mainFrame = tk.Frame(self, bg="#AC99F2")
        self.mainFrame.pack(fill="both", expand=True)

        Label(self, text="IP: 192.168.1.7").pack()
        Label(self, text="PORT: 39000").pack()

        # ICON
        app_icon = Image.open("ClientMaterial/dulich.jpg")
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)

        # Scroll bar of main frame
        scrollBarTreeView = Scrollbar(self.mainFrame)
        scrollBarTreeView.pack(side=RIGHT, fill=Y)
        scrollBarTreeView = Scrollbar(self.mainFrame, orient="horizontal")
        scrollBarTreeView.pack(side=BOTTOM, fill=X)

        # Treeview
        treeView = ttk.Treeview(
            self.mainFrame,
            yscrollcommand=scrollBarTreeView.set,
            xscrollcommand=scrollBarTreeView.set,
        )
        treeView.pack()

        # Config Scroll Bar to TreeView
        scrollBarTreeView.config(command=treeView.yview)
        scrollBarTreeView.config(command=treeView.xview)

        # Define column of Treeview
        treeView["columns"] = (
            "Code",
            "Location",
            "Longitude",
            "Latitude",
            "Address",
            "Description",
        )

        # Format column of Treeview
        treeView.column("#0", width=0, stretch=NO)
        treeView.column("Code", anchor=CENTER, width=50)
        treeView.column("Location", width=400)
        treeView.column("Longitude", anchor=CENTER, width=200)
        treeView.column("Latitude", anchor=CENTER, width=200)
        treeView.column("Address", anchor=CENTER, width=200)
        treeView.column("Description", anchor=CENTER, width=200)

        # Create Headings
        treeView.heading("#0", text="", anchor=CENTER)
        treeView.heading("Code", text="Code", anchor=CENTER)
        treeView.heading("Location", text="Location", anchor=CENTER)
        treeView.heading("Longitude", text="Longitude", anchor=CENTER)
        treeView.heading("Latitude", text="Latitude", anchor=CENTER)
        treeView.heading("Address", text="Address", anchor=CENTER)
        treeView.heading("Description", text="Description", anchor=CENTER)

        def handle_queryBtnClick(event):
            global userChoose
            userChoose = int(treeView.selection()[0]) - 1

        # Load data from File
        with open(
            f"{CLIENT_TMP_FOLDER}/{SERVER_FILE_LISTDATA_NAME}", "rb"
        ) as fDataList:
            myjson = fDataList.read().decode()
            jsonDataList = json.loads(myjson)

            # Dont know why x = 1
            x = 1
            for field in jsonDataList:
                code = field["code"]
                loca = field["location"]
                lon = field["longitude"]
                lat = field["latitude"]
                addr = field["address"]
                des = field["description"]

                # Add data to Treeview
                treeView.insert(
                    parent="",
                    index="end",
                    iid=x,
                    text="",
                    values=(code, loca, lon, lat, addr, des),
                )

                x = x + 1

                treeView.pack()

        queryBtn = Button(
            self, text="Select", command=lambda: self.showInformationAddress()
        )
        queryBtn.pack()
        queryBtn.bind("<Button-1>", handle_queryBtnClick)

        self.mainloop()

    def downListData(self):
        if os.path.isfile(f"{CLIENT_TMP_FOLDER}/{SERVER_FILE_LISTDATA_NAME}") == True:
            print(f"[*] File {SERVER_FILE_LISTDATA_NAME} is on {CLIENT_TMP_FOLDER}")
            return

        s = socket(AF_INET, SOCK_DGRAM)

        s.sendto(QUERY_LISTDATA.encode(), SERVER_ADDRESS_PORT)
        print(
            f"[-] Send {QUERY_LISTDATA} to address {SERVER_ADDRESS_PORT[0]} at port {SERVER_ADDRESS_PORT[1]}"
        )

        data, Addr_Port = s.recvfrom(1024)
        print(
            f"[-] Receive {data.decode()} from address {Addr_Port[0]} at port {Addr_Port[1]}"
        )

        fDataList = open(f"{CLIENT_TMP_FOLDER}/{data.decode()}", "wb")
        data, Addr_Port = s.recvfrom(1024)
        try:
            while data:
                fDataList.write(data)
                s.settimeout(0.1)
                data, Addr_Port = s.recvfrom(1024)
        except timeout:
            fDataList.close()
            s.close()
            print(
                f"[!] File {SERVER_FILE_LISTDATA_NAME} had downloaded from address {Addr_Port[0]} at port {Addr_Port[1]}"
            )
            # messagebox.showinfo("Load File", "Finish")

    def downOneImage(self):
        s = socket(AF_INET, SOCK_DGRAM)

        with open("ClientTmp/ListData.json", "rb") as f:
            data = f.read().decode("utf-8")
            my_json = json.loads(data)

            for j in range(0, len(my_json[userChoose].get("image"))):
                # Check if image is on CLientTmp
                imageFileName = my_json[userChoose].get("image")[j]
                if os.path.isfile(f"{CLIENT_TMP_FOLDER}/{imageFileName}") == True:
                    print(f"[*] Image {imageFileName} is on {CLIENT_TMP_FOLDER}")
                    continue

                isImageLoad = False

                while not isImageLoad:
                    command = QUERY_IMAGE_prefix + str(userChoose + 1) + "_" + str(j)

                    s.sendto(command.encode(), SERVER_ADDRESS_PORT)
                    print(
                        f"[*] Send {command} to address {SERVER_ADDRESS_PORT[0]} at port {SERVER_ADDRESS_PORT[1]}"
                    )

                    data, addr = s.recvfrom(1024)
                    print(f"[*] Receive from address {addr[0]} at port {addr[1]}")

                    pathImage = f"{CLIENT_TMP_FOLDER}/{data.decode()}"
                    fImageData = open(pathImage, "wb")

                    # Download Image
                    try:
                        while dataAddr := s.recvfrom(1024):
                            fImageData.write(dataAddr[0])
                            s.settimeout(0.1)

                    except timeout:
                        fImageData.close()
                        print(f"[*] Done {command}")

                    # Try open file
                    # If it corrupted, redownload
                    try:
                        ImageTk.PhotoImage(Image.open(pathImage))
                        print(f"[*] The {pathImage} has loaded")
                        isImageLoad = True

                    except Exception as exception:
                        print(f"[!] {exception}")

    def showInformationAddress(self):
        # self.loadFileFromServer()

        root = Toplevel()
        root.geometry("1040x480")
        root.title("Information")
        root.resizable(False, False)

        app_icon = Image.open("ClientMaterial/dulich.jpg")
        app_icon = ImageTk.PhotoImage(app_icon)
        root.iconphoto(False, app_icon)

        # BACKGROUND
        background = Image.open("ClientMaterial/backgroundInformation.jpg")
        background = background.resize((1040, 480), Image.ANTIALIAS)
        root.background = ImageTk.PhotoImage(background)
        Label(root, image=root.background).place(x=0, y=0)

        # code location address longitude latitude description
        with open("ClientTmp/ListData.json", "rb") as f:
            data = f.read().decode("utf-8")
            my_json = json.loads(data)

            title_code = Label(
                root,
                text="MÃ SỐ",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_code.grid(row=1, column=0, sticky="W")
            code = Text(
                root, width=40, height=1, font=("times new roman", 15), wrap=WORD
            )
            code.tag_configure("center", justify="center")
            code.bind("<Key>", lambda e: "break")
            code.grid(row=1, column=1, padx=10, pady=15)
            code.insert(tk.INSERT, (my_json[userChoose].get("code")))

            title_location = Label(
                root,
                text="TÊN ĐỊA ĐIỂM",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_location.grid(row=2, column=0, sticky="W")
            location = Text(
                root, width=40, height=2, font=("times new roman", 15), wrap=WORD
            )
            location.tag_configure("center", justify="center")
            location.bind("<Key>", lambda e: "break")
            location.grid(row=2, column=1, padx=10, pady=15)
            location.insert(tk.INSERT, str(my_json[userChoose].get("location")))

            title_address = Label(
                root,
                text="ĐỊA CHỈ",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_address.grid(row=3, column=0, sticky="W")
            address = Text(
                root, width=40, height=2, font=("times new roman", 15), wrap=WORD
            )
            address.tag_configure("center", justify="center")
            address.bind("<Key>", lambda e: "break")
            address.grid(row=3, column=1, padx=10, pady=15)
            address.insert(tk.INSERT, str(my_json[userChoose].get("address")))

            title_longitude = Label(
                root,
                text="KINH ĐỘ",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_longitude.grid(row=4, column=0, sticky="W")
            longitude = Text(
                root, width=40, height=1, font=("times new roman", 15), wrap=WORD
            )
            longitude.tag_configure("center", justify="center")
            longitude.bind("<Key>", lambda e: "break")
            longitude.grid(row=4, column=1, padx=10, pady=15)
            longitude.insert(tk.INSERT, str(my_json[userChoose].get("longitude")))

            title_latitude = Label(
                root,
                text="VĨ ĐỘ",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_latitude.grid(row=5, column=0, sticky="W")
            latitude = Text(
                root, width=40, height=1, font=("times new roman", 15), wrap=WORD
            )
            latitude.tag_configure("center", justify="center")
            latitude.bind("<Key>", lambda e: "break")
            latitude.grid(row=5, column=1, padx=10, pady=15)
            latitude.insert(tk.INSERT, str(my_json[userChoose].get("latitude")))

            title_description = Label(
                root,
                text="MÔ TẢ",
                font=("times new roman", 15, "bold"),
                fg="#000",
                bg="#FAFAFA",
            )
            title_description.grid(row=6, column=0, sticky="W")

            description = Text(
                root, width=40, height=5, font=("Times New Roman", 15), wrap=WORD
            )
            description.tag_configure("center", justify="center")
            description.bind("<Key>", lambda e: "break")
            description.grid(row=6, column=1, padx=10, pady=15)

            scrollbar = tk.Scrollbar(root, command=description.yview)
            scrollbar.grid(row=6, column=2, sticky="ns")

            description.insert(tk.INSERT, str(my_json[userChoose].get("description")))

            self.downOneImage()
            # roott = Toplevel()

            imageNumber = 0

            imageName = my_json[int(code.get("1.0", END)) - 1].get("image")[imageNumber]
            my_img = ImageTk.PhotoImage(
                Image.open(f"{CLIENT_TMP_FOLDER}/{imageName}").resize(
                    (380, 280), Image.ANTIALIAS
                )
            )

            label = Button(root, image=my_img, command=lambda: zoomImage(imageNumber))
            # lbl.image = my_img
            label.grid(row=1, column=3, columnspan=2, rowspan=6, padx=35, pady=5)

            def zoomImage(image_number):


                # top = Toplevel()
                # x = 980
                # y = 580
                # top.geometry(f"{x}x{y}")
                # top.title("Information")
                # top.resizable(False, False)

                # app_icon1 = Image.open("ClientMaterial/dulich.jpg")
                # app_icon1 = ImageTk.PhotoImage(app_icon1)
                # top.iconphoto(False, app_icon1)

                # Background
                imageName = my_json[int(code.get("1.0", END)) - 1].get("image")[
                    image_number
                ]
                # my_img = ImageTk.PhotoImage(
                #     Image.open(f"{CLIENT_TMP_FOLDER}/{imageName}").resize(
                #         (x, y), Image.ANTIALIAS
                #     )
                # )
                MainWindowZoom(Toplevel(), f"{CLIENT_TMP_FOLDER}/{imageName}")
                # top.background = my_img

                # Label(top, image=top.background).place(x=0, y=0)

                # top.protocol("WM_DELETE_WINDOW", lambda: handle_BtnExit(top))
                # top.mainloop()

            def forward(image_number):
                global label
                global button_forward
                global button_back
                # x = 380
                # y = 280
                # label.grid_forget()

                # Load Image
                imageName = my_json[int(code.get("1.0", END)) - 1].get("image")[
                    image_number
                ]
                my_img = ImageTk.PhotoImage(
                    Image.open(f"{CLIENT_TMP_FOLDER}/{imageName}").resize(
                        (380, 280), Image.ANTIALIAS
                    )
                )
                label = Button(
                    root, image=my_img, command=lambda: zoomImage(image_number)
                )
                label.image = my_img

                # Load Button Forward
                button_forward = Button(
                    root, text=">>", command=lambda: forward((image_number + 1))
                )

                button_back = Button(
                    root, text="<<", command=lambda: back(image_number - 1)
                )

                if image_number == 2:
                    button_forward = Button(root, text=">>", state=DISABLED)

                label.grid(row=1, column=3, columnspan=2, rowspan=6, padx=35, pady=5)
                button_back.grid(row=6, column=3)
                button_forward.grid(row=6, column=4)

            def back(image_number):
                global my_label
                global button_forward
                global button_back

                # my_label.grid_forget()
                # x = 380
                # y = 280
                # my_label.grid_forget()

                imageName = my_json[int(code.get("1.0", END)) - 1].get("image")[
                    image_number
                ]
                my_img = ImageTk.PhotoImage(
                    Image.open(f"{CLIENT_TMP_FOLDER}/{imageName}").resize(
                        (380, 280), Image.ANTIALIAS
                    )
                )
                label = Button(
                    root, image=my_img, command=lambda: zoomImage(image_number)
                )
                label.image = my_img

                button_forward = Button(
                    root, text=">>", command=lambda: forward((image_number + 1))
                )
                button_back = Button(
                    root, text="<<", command=lambda: back(image_number - 1)
                )

                if image_number == 0:
                    button_back = Button(root, text="<<", state=DISABLED)

                label.grid(row=1, column=3, columnspan=2, rowspan=6, padx=35, pady=5)
                button_back.grid(row=6, column=3)
                button_forward.grid(row=6, column=4)

            button_back = Button(
                root, text="<<", command=lambda: back(imageNumber - 1), state=DISABLED
            )
            button_forward = Button(
                root, text=">>", command=lambda: forward(imageNumber + 1)
            )
            button_back.grid(row=6, column=3)
            button_forward.grid(row=6, column=4)

        root.mainloop()
        # root.destroy()


FirstScreen()
