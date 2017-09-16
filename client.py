import socket
import sys
import json
import traceback
from _thread import *

#This is the DICT which I am using to send as an JASON object to comunicate with server.
outgoing={"sign-in-bol":False,#This is set to TRUE when client want to sign-in.
          "list-bol":False,#This is set to TRUE when client want to send LIST command.
          "send-bol":False,#This is set to TRUE when client want to send SEND command.
          "sign-in":"",#Here username of client is send so that server can mantain the record of user.
          "send":""}#Here the username whom the client want to send message.
#This is the DICT which I am using to send as an JASON object to communivate with other peers.
peer_out={"list-respons":False,#This will always remain FALSE but I need them so that NULLERROR is not created in recieving thread
          "send-reply":False,#This will always remain FALSE but I need them so that NULLERROR is not created in recieving thread
          "msg-incoming":False,#This is set to TRUE when client sends message to other client(peer)
          "username":"",#Here client will store it's username so that other client knows who is sending the message.
		  "message":""}#Here the message which is supposed to be sent is attached.
#Here I will store the message client want to send to other client.
msg_send=""

#This function is first function which is called when program is execute. This creates a
#socket and returns the created socket
def socket_creation():
    try:
        #Create a socket which will comunicate using UDP packet.
        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    except Exception:
        #This prints the describtion of exception and the traces the stack for last call.
        print(traceback.format_exc())
    #This checks that arguments passed while executing the code are valid or not.
    if len(sys.argv)==7 and sys.argv[1]=="-u" and sys.argv[3]=="-sip" and sys.argv[5]=="-sp" and  int(sys.argv[6])<=65536 and int(sys.argv[6])>=0:
        return udp_socket
    else:
        print("6 arguments are excepted")
        print("Format is: python example.py -u USERNAME -sip IP -sp PORTNUMBER[0-65536]")
        exit()

#This sends server info of user like Username so that server can store info.
def sign_in(socket_obj):
    outgoing["sign-in-bol"]=True
    outgoing["sign-in"]=sys.argv[2]
    json_obj=json.dumps(outgoing,ensure_ascii=False)+"-e"
    udp_socket.sendto(json_obj.encode('utf-8'),(sys.argv[4],int(sys.argv[6])))
    incoming=socket_obj.recvfrom(2048)
    recieved_obj=json.loads(incoming[0].decode())
    if recieved_obj["sign-in-status"]:
        print("Login Successfull")
    else:
        print("Username already Exist. Please try again with different Username")
        exit()
    outgoing["sign-in-bol"]=False

#This method is called when user enters "LIST" command.
def enq_list(socket_obj):
    outgoing["list-bol"]=True
    json_obj=json.dumps(outgoing,ensure_ascii=False)+"-e"
    udp_socket.sendto(json_obj.encode('utf-8'),(sys.argv[4],int(sys.argv[6])))
    outgoing["list-bol"]=False

#This method is called when user enters "SEND" command.
def send_msg(socket_obj, username,message):
    msg=" ".join(message)
    outgoing["send-bol"]=True
    outgoing["send"]=username
    json_obj=json.dumps(outgoing,ensure_ascii=False)+"-e"
    udp_socket.sendto(json_obj.encode('utf-8'),(sys.argv[4],int(sys.argv[6])))
    outgoing["send-bol"]=False

#This is the method which runs on it's own Thread. It keeps listening on port for
#incoming message on the port.
def peer_listen(socket_obj,temp):
    print("--------------Recieve Thread-----------------")
    try:
        while 1:
            incoming = socket_obj.recvfrom(2048)
            if incoming:
                recieved_obj=json.loads(incoming[0].decode())
                if recieved_obj["list-respons"]:
                    print(recieved_obj["list"])
                elif recieved_obj["send-reply"]:
                    peer_out["msg-incoming"]=True
                    peer_out["username"]=sys.argv[2]
                    peer_out["message"]=msg_send
                    json_obj=json.dumps(peer_out,ensure_ascii=False)
                    udp_socket.sendto(json_obj.encode('utf-8'),tuple(recieved_obj["send"]))
                    peer_out["msg-incoming"]=False
                    peer_out["username"]=""
                    peer_out["message"]=""
                elif recieved_obj["msg-incoming"]:
                    print("<From ",incoming[1],":",recieved_obj["username"],">: ",recieved_obj["message"])
    except Exception:
        print(traceback.format_exc())

#Calls socket_creation() for creating the socket.            
udp_socket=socket_creation()
#Calls sign_in so that server knows the username loged in.
sign_in(udp_socket)
#Creates a new Thread who's only job is to listen on port.
start_new_thread(peer_listen,(udp_socket,54))
while 1:
    message=input()
    if message.split(" ")[0]=="list":
        enq_list(udp_socket)
    elif message.split(" ")[0]=="send":
        msg_send=" ".join(message.split(" ")[2:])
        send_msg(udp_socket,message.split(" ")[1],message.split(" ")[2:])
    else:
        print("Wrong Input")
udp_socket.close()
        
        
        
