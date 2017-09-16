Server:
Server will create a scoket an bind it with local IP and port-number which is provided by user.I have created a seperate thread on which it will listen for incoming udp packet on that port.It will reply accordingly to the client command.Here I have used JSON for serializing the data I am sending and recieving data. The meaning of each field in JSON
is explained by comments in code. 

Client:
Here I have used 2 different thread one for sending Commands/Message to Server/Peer and other for recieveing reply from
Server/Peer. Here I have also used JSON for communication. This is sending message to other client on it's own and server doesn't know what message was send to other client.

Python version:3.5.2
Libraries: JSON, SYS, SOCKET, TRACEBACK, _thread

First run server by following command:
python server.py -sp PORT-NUMBER

Then open any number of client(but different username) by following command:
python client.py -u USERNAME -sip IP-ADDRESS -sp PORTNUMBER

after use any combination of LIST and SEND command on client side.
