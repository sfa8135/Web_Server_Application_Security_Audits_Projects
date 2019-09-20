import sys
VERSION= 'HTCPCP-TEA/1.0'  
CRLF = '' # =\n\r
StatusCode = " " 
ForCoffee = False

# this function for request line parsing  
def Requestline(data):
#first divide the request line to its main component
    div = data.split(" ")
    method = div[0]
    URI = div[1]
    version = div[2]
# chack if it is using a valid/supported method
    methods = ["GET", "POST", "DELETE", "OPTIONS", "HEAD", "PUT", "DELETE", "TRACK", "BREW", "WHEN", "PROFIND"]
    if method not in methods: print("Syntax Error!")

#divide URI and chack if it follow valid syntax and entries 
    Tea =["peppermint","black","green","earl-grey"]
    XTea =["chai","rasepberry","oolong"] 
    addition = ["Cream", "Half-and-half", "Whole-milk", "Part-Skim","Skim", "Non-Dairy","Vanilla", "Almond", "Raspberry","Chocolate", "Whisky", "Rum", "Kahlua", "Aquavit"]
       
    global StatusCode
    global ForCoffee
    
    if method == "BREW" or method == "POST":
     
     if URI == '/': StatusCode = "300 Multiple Options"
     else: 
      divURI=URI.split("/")
      if len(divURI) == 2: 
          ForCoffee=True 
          

      else:
       if divURI[2] in XTea: StatusCode = "403 Forbidden"
       elif divURI[2] not in Tea: StatusCode = "403 Forbidden"
    
    elif method == 'GET':
        divURI=URI.split("?") #we divide the get to extract the query
        if len(divURI) > 1:  #validate if there is indeed query or not
         query = divURI[1]   #if yes, we assign it to 'query'
         divQuery = query.split("&") # we check if this query has multiple addition
         
         if len(divQuery) > 1: #if yes, we wanna check that all of them are valid
             
             for x in divQuery:
                if x not in addition: 
                    StatusCode ="403 Forbidden"
         else:   
              if query not in addition: StatusCode ="403 Forbidden"

          
# correct version?
    if version != VERSION: print("Syntax Error!")

    
#this function for header parsing
def Header(data):
    addition = ["Cream", "Half-and-half", "Whole-milk", "Part-Skim","Skim", "Non-Dairy","Vanilla", "Almond", "Raspberry","Chocolate", "Whisky", "Rum", "Kahlua", "Aquavit"]
    global StatusCode
    global ForCoffee
#make sure that the cotnet type and the accept addition has valid entries 
    div=data.split(":")
    if div[0] =='Content-Type': 
         if div[1] == 'message/coffee-pot-command': StatusCode= "418 I'm a Teapot"
         elif div[1] == 'message/teapot' and ForCoffee:  
             StatusCode= "400 Bad Request" 
             
         elif div[1] != 'message/teapot': StatusCode ="403 Forbidden"  

    if div[0] == 'Accept-Addition':
        extra=div[1].split(";")
        if len(extra) > 1: 
            for x in extra:
                if x not in addition: 
                    StatusCode ="403 Forbidden"
        else:   
         if div[1] not in addition: StatusCode ="403 Forbidden"
             

        
#this function for body parsing. if any
def Body(data):
     print("")
     


def main():
  #the main function will read the request file and divide its content to 3 function: request line, header and body
  filename = sys.argv[1]
  file = open(filename)
  filedata = file.read()

  lines = filedata.split("\n")
  Requestline(lines[0])
  count = 1

  if lines[count] != CRLF:
      while lines[count] != CRLF:
       Header(lines[count]) 
       count=count+1
  
  if lines[count]!= CRLF:
      print("Syntax Error!")
      
  count=count+1 
  if lines[count] != CRLF:    
      Body(lines[count])

  #if no error code is generated, it means everything is ok =200
  global StatusCode 
  if StatusCode==" ": StatusCode="200 OK"
  #after return from these functions. it is time for sending the response    
  Response = VERSION + " " +StatusCode + CRLF + CRLF 
  print(Response)

main()