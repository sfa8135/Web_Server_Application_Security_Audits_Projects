#this code is to analyse the htcpcp-tea request 
#and based on the infrmation provided either a file with jason would be created or an error status code
#we will create also log file to keep track of entered header infromation 

import json
import os 
import logging
import requests


#this function suppose to be called by the server given a request and generated a response accordingly
def parse_request(request):
 # define global variable and arrys that will be used below 
 CRLF = "" #"\r\n"
 StatusCode = " " #final result
 ForCoffee = False  #tea by default
 BrewIssued=False   #in case get generated before brew
 #to compare addition with the accepted ones 
 addition = ["Cream", "Half-and-half", "Whole-milk", "Part-Skim","Skim", "Non-Dairy","Vanilla", "Almond", "Raspberry","Chocolate", "Whisky", "Rum", "Kahlua", "Aquavit"]
 #get current working dirextory for creating fileor directory based on information provided
 path= os.getcwd()


 #first define the request line and the header by seperating the request into lines
 line=request.split("\n")
 
 #to make sure that there is no get request issued before brew request and to keep track of the system, we create log file
 logging.basicConfig(filename="logheader.log", level=logging.INFO)
 logger=logging.getLogger()
 logger.info(line[0])


 #--------------- This is parsing the Request line ------------------------------------------------
 # solve q5 a,b
 URI= ""
 method=""
 #divide the first line which is the request line to parts to investigate the method and the URI
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
    if BrewIssued== False: StatusCode="404 not found"

 if method=="POST": StatusCode="400 Bad Request" #q8

 #--------------- This is parsing the Header -------------------------------------------
 
 addi= list()#in this array, we will sign the addition to send it later to jason file
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
 
 #q10
 if CT=="C" and ForCoffee==False: StatusCode="418 I'm a teapot"
 elif CT=="T" and ForCoffee: StatusCode="400 Bad Request"

 #q9 here we assign value for the type and veraity to transfer it to json file
 typee= ""
 if ForCoffee: typee="coffee"
 elif ForCoffee==False: typee="tea"   
 variety=""
 if typee=="tea" and method=="BREW": variety=divURI[2] 

 resCT =" "
 if typee=="tea": resCT ="Content-Type: message/teapot"
 elif typee=="coffee": resCT ="Content-Type: message/coffee-pot-response"

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
    
 
    
    
 return response


