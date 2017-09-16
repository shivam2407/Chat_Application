
import socket
import sys
import json
import traceback
from _thread import *

#This is the Dictionary where server will store info about User like: Username,IP and Port.
client_record={}

#This is the DICT which is used to send JASON data to other clients.
outgoing={"list-respons":False,#This is set to TRUE when server sends reply in response to LIST command.
          "send-reply":False,#This is set to TRUE when server sends reply in response to SEND command.
          "sign-in-status":False,#This is set to TRUE if no pre-existing username is thier in server database.
          "list":[],#The list of user is attached here when server is replying in response to LIST command.
		  "send":()}#The tuple of (IP,PORT_NUMBER) for the username requested by client is attached here.

#This function is first function which is called when program is execute. This creates a
#socket and binds it with local IP and port number provided by user.
def socket_creation():
    try:
        #Create a socket which will comunicate using UDP packet.
        udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    except Exception:
        #This prints the describtion of exception and the traces the stack for last call.
        print(traceback.format_exc())
        
    #This checks that arguments passed while executing the code are valid or not.
    if len(sys.argv)==3 and sys.argv[1]=="-sp" and int(sys.argv[2])<=65536 and int(sys.argv[2])>=0:
        udp_socket.bind((" ",int(sys.argv[2])))
        return udp_socket
    else:
        print(sys.argv[1],"  ",int(sys.argv[2]))
        print("2 arguments are excepted")
        print("Format is: python example.py -sp PORTNUMBER[0-65536]")
        exit()# The program stops if arguments are not valid

        
#This method countiously listen on socket to recieve message from different clients. It
# is created on different thread.        
def listen_4_client(socket_obj, temp):
    print("-----Inside Thread---------")
    final_message=""
    while 1:
        try:
            incoming = socket_obj.recvfrom(2048)
            if incoming:
                incoming_message=incoming[0].decode()
				#Here "-e" is the end of line command and so if I dont get "-e" at the end 
				#of message that means thier is still some message left to revieve
                if(incoming[0].decode()[-2:]!="-e"):
					#I am appending the incoming new message to last message so that in the 
					#end we can use the whole message together.
                    final_message+=incoming_message
                    continue
                else:
					#Here I have removed "-e" from end so that while parsing json no error ocurs 
                    final_message+=incoming_message[:-2]    
                recieved_obj=json.loads(final_message)
                if recieved_obj["sign-in-bol"]:
                    print(incoming[1])
                    if recieved_obj["sign-in"] not in client_record.keys():
                        client_record[recieved_obj["sign-in"]]=incoming[1]
                        outgoing["sign-in-status"]=True
                    json_obj=json.dumps(outgoing,ensure_ascii=False)
                    socket_obj.sendto(json_obj.encode('utf-8'),incoming[1])
                    outgoing["sign-in-status"]=False
                elif recieved_obj["list-bol"]:
                    print(incoming[1])
                    outgoing["list"]=list(client_record.keys())
                    outgoing["list-respons"]=True
                    json_obj=json.dumps(outgoing,ensure_ascii=False)
                    socket_obj.sendto(json_obj.encode('utf-8'),incoming[1])
                    outgoing["list"]=[]
                    outgoing["list-respons"]=False
                elif recieved_obj["send-bol"]:
                    outgoing["send-reply"]=True
                    outgoing["send"]=client_record[recieved_obj["send"]]
                    json_obj=json.dumps(outgoing,ensure_ascii=False)
                    socket_obj.sendto(json_obj.encode('utf-8'),incoming[1])
                    outgoing["send"]=()
                    outgoing["send-reply"]=False
                final_message=""
        except Exception:
            print(traceback.format_exc())                   
                

#Calling socket_creation() function to create socket and it returns the socket obj.
server_soc=socket_creation()
print("-------------STarted Listening-----------------")
#This creates a new thread for listening on port.Here 52 is just passed to make it a tuple. 
start_new_thread(listen_4_client,(server_soc, 52))
while 1:
    pass
server_soc.close()                      
