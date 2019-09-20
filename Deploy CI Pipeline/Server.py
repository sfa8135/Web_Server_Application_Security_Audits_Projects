#this goal of this code is to capture the header by the server and then execute PHP script to send the result to the user
#in this code, we used socket and threading libraries 
#to create a server that parse a HTCPCP request and generate a response accordingly 
# we used also sys libraries to get 2 command argument from the user: IP and port that server listen to 

import socket 
import threading
import json
import os
import logging
import requests
import sys
import subprocess

ip = sys.argv[1] 
bind_port = sys.argv[2]
port=int(bind_port)

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
print "[*] listening on %s:%d" %(ip,port)

def handle_client(client_socket):

    request=client_socket.recv(1024)
    print "[*] Received: %s" %request
    #here we will send the request to another function to parse the request and return the appropriate status code
    result=parse(request)
    code="statusCode="+result+" HTCPCP-TEA/1.0"
    #after the status code has been return, we will send it to the php file using php-cgi
    response1= subprocess.check_output(['php-cgi','p.php',code])
    #the result for this code will be returned to the user via the browser
    client_socket.send(response1)
    client_socket.send(response2)
    client_socket.close()

def parse(request):
 global response2
 response2= subprocess.check_output(["php","/var/www/html/p.php","HI"])
 CRLF = "" #"\r\n"
 StatusCode = " " #final result
 ForCoffee = False  #tea by default
 BrewIssued=False   #in case get generated before brew 
 addition = ["Cream", "Half-and-half", "Whole-milk", "Part-Skim","Skim", "Non-Dairy","Vanilla", "Almond", "Raspberry","Chocolate", "Whisky", "Rum", "Kahlua", "Aquavit"]
 path= os.getcwd()
 
 line=request.split("\n")
  
 logging.basicConfig(filename="logheader.log", level=logging.INFO)
 logger=logging.getLogger()
 logger.info(line[0])


 #--------------- This is parsing the Request line ------------------------------------------------
 
 
 URI= ""
 # now we send the URI to the PHP script if the method is GET and not POST
 os.environ['URI']=URI 
 #subprocess.check_output(['php-cgi','p.php',os.environ['URI']])
 method=""
 reqline = line[0].split(" ")
 

 if len(reqline)>1:
  method = reqline[0]
  URI = reqline[1]
 #version = reqline[2]
 
 

 #determine if the request for tea or coffee 
 divURI=URI.split("/")
 if URI == '/': StatusCode = "300 Multiple Options"   
 else: 
     if len(divURI) == 2: 
         ForCoffee=True
 
 if method == "BREW":   # if brew request is issued, then we will see if it is coddee(create file) or tea(create a folder and file inside)
  if ForCoffee: C= open(divURI[1],"w+") # if coffee we will create a file name the same as the pot-#    
  elif ForCoffee==False:   #if it is tea, we will vreate a directory but first wanna make sure that this specific pot was not used before
   path= path + "/" + divURI[1]
   try: os.mkdir(path) # if the pot was already used and a file or director has been created for it will generate 403
   except OSError:  StatusCode= "403 Forbidden" #or you can count the file#. if len(os.listdir(path))>1, means there is another file and sourceCode=403  
   else:
    os.chdir(path) #if not, create a brand new folder and create a file inside it by the name of the tea type
    T = open(divURI[2],"w+") 
 #q7 check if additions are accepted 
 if method=="GET": 
    check=URI.split("?")
    if len(check) > 1: #make sure there is query
        global query
        query = check[1]
        divQuery = query.split("&")
        if len(divQuery) > 1:
            for x in divQuery:
             if x not in addition: 
              StatusCode ="403 Forbidden"
        else:   
             if query not in addition: StatusCode ="403 Forbidden"
                 
    
    for x in os.listdir(path): #q6: check A GET request for a uri for which a BREW request has not yet been issued should produce a response code 404.
     if x == divURI[1]+".py" or x == divURI[1]: BrewIssued =True
   # if BrewIssued== False: StatusCode="404 not found"

 if method=="POST": StatusCode="400 Bad Request" #q8
 
 addi= list() #in this array, we will sign the addition to send it later to jason file
 CT=""
 count = 1
 if len(line)>1:
  if line[count] != CRLF:
   while line[count] != CRLF:  #here we trying to parse the header line by line. once it face CRLF that means the end of the header, and it will stop 
    header=line[count].split(":") #then we divide the header to extract the content type and the accept addition
    if header[0]=='Content-Type': 
      if header[1].strip()=="message/teapot": CT="T" #CT is short for content type to determine the type which will help later
      if header[1].strip()=="message/coffee-pot-command": CT="C"    
    if header[0]=='Accept-Additions': #divide addition by & to extract the addition for jason file wheather it is 1 or many 
      Hpart=header[1].split(";") #x=len(Hpart) # Hpart.strip()
      if len(Hpart)>1:
          for x in Hpart:
              addi.append(x)
      else: addi.append(Hpart)
    count=count+1
 
 if CT=="C" and ForCoffee==False: StatusCode="418 I'm a teapot"
 elif CT=="T" and ForCoffee: StatusCode="400 Bad Request"

 #q9 here we assign value for the type and veraity to transfer it to json file
 typee= ""
 if ForCoffee: typee="coffee"
 elif ForCoffee==False: typee="tea"   
 variety=""
 if typee=="tea" and method=="BREW": variety=divURI[2] 

 resCT =" "
 if typee=="tea":
  # sending to the php code the type wheather it is tee or coffee   
  resCT ="Content-Type: message/tea-pot-response"
  response2= subprocess.check_output(["php","/var/www/html/p.php",resCT])
 
 elif typee=="coffee":
  resCT ="Content-Type: message/coffee-pot-response"
  response2= subprocess.check_output(["php","/var/www/html/p.php",resCT])


 #Buil dictionery to add type,variety,addition to JSON file
 data = {}
 data['type'] = typee
 if variety!="": data['variety'] = variety
 data["Additions:"]= {}  #build nested dictionery
 for i in range (0,len(addi),1):
    data["Additions:"]["addition"+str(i)]=addi[i].strip() #strip to remove the additional unwanted space
 json_data = json.dumps(data) #send dictionery to build json data 
 if method == "BREW":
  if ForCoffee: C.write(json_data) #C and T represents two files that has been created previously for coffee and tea 
  else: T.write(json_data)
      
 if URI == '/': StatusCode = "300 Multiple Options" 
 
 if StatusCode==" ": StatusCode="200 OK" # if after been through all condition and SC is the same => 200
 if StatusCode!="200 OK": resCT=" "
 response= "\n\n" + StatusCode + "\n\n" +resCT+ "\n\n"
 return StatusCode 

while True:
    client,addr =server.accept()
    print "[*] Accept connection from %s:%d" %(addr[0],addr[1])
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
    
