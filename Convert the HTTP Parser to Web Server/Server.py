#in this code, we used socket and threading librbaries 
#to create a server that interact with a HTCPCP parser and generate a response accordingly 
# we used also sys libraries to get 2 command argument from the user: IP and port that server listen to 
# then we send the generated request to the parser function to anther python file called parser 

# first we import the prasing function from the other file: parser
from Parser import parse_request
import sys
import socket 
import threading

#we convert the giving data by the user just to make sure it follow the right format
bind_ip= sys.argv[1] 
ip= str(bind_ip)

bind_port= sys.argv[2]
port=int(bind_port)

#creating server using socket
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(1)
print "[*] listening on %s:%d" %(ip,port)


#this is our client-handling thread
def handle_client(client_socket):

    #print what the client send
    request=client_socket.recv(1024)
    print "[*] Received: %s" %request
    response=parse_request(request)

    #send back a packet 
    client_socket.send(response)
    client_socket.close()

#this is for different thread
while True:
    client,addr =server.accept()
    print "[*] Accept connection from %s:%d" %(addr[0],addr[1])
    # spin up our client thread to handle incoming data
    #client_handler = threading.Thread(target=handle_client,args=(client,))
    #client_handler.start()
    handle_client(client)
