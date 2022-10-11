import socket
import time
import threading
from tkinter import *

# connection variables for server
PORT = 4050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISC_MSG = "!DISCONNECT"

# define server variables
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

# create GUI
root = Tk()
root.geometry("300x500")
root.config(bg = "white")
root.wm_title("Encrypted P2P Messanger")

#Communication
def func():
    lstBox.insert(0,"[STARTING] server is starting...")
    print("here")
    lstBox.insert(0, f"[LISTENING] Server is listening on {SERVER}")
    while True:

        conn,address = server.accept()
        th = threading.Thread(target=recv, args=(conn, address))
        th.start()
        lstBox.insert(0,f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def recv(conn,address):
    lstBox.insert(0, "[NEW CONNECTION] {addr} connected.")
    connected  = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISC_MSG:
                connected = False

            lstBox.insert(0,f"[{address}] {msg}")
            print()
            conn.send("Msg received".encode(FORMAT))
    conn.close()

def threadSendMsg() :
    th = threading.Thread(target=sendMsg)
    th.start()

def sendMsg():
    global s
    if s == 0:
        s = socket.socket()
        hostname = 'Gayana'
        port = 4050
        s.connect((hostname,port))
        msg = massagebox.get()
        lstBox.insert(0, "You : "+msg)
        s.send(msg.encode())
        s = s+1

    else:
        msg = massagebox.get()
        lstBox.insert(0,"You : "+msg)
        s.send(msg.encode())

#import images
startChatImg = PhotoImage(file = "startchat.png")
sendMsgImg = PhotoImage(file = 'sendMsg.png')

#define object components
lstBox = Listbox(root, height = 20, width = 43)
lstBox.place(x = 15, y=120)

labelHeader = Label(root, text = "Secure Chat APP", font=("Helvetica", 18), bg = "white")
labelHeader.place(x = 5, y = 2);

buttons = Button(root, image = startChatImg, command = func, borderwidth = 0)
buttons.place(x = 75, y = 40)

massage = StringVar()
massagebox = Entry(root ,textvariable = massage ,font = ('claibre',10,'normal'), border = 2, width = 32)
massagebox.place(x = 10, y = 464)

sendMsgBtn= Button(root, image = sendMsgImg, command = threadSendMsg, borderwidth= 0)
sendMsgBtn.place(x = 260, y=460)


root.mainloop()



