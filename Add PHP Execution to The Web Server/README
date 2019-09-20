In this folder you will find: a source code written in python(server) and PHP file (HTCPCP) 
also a screenshot that illustrate the default output in case of a GET response for a tea 

the server will invoke php-cgi and execute server-side code written in PHP. 
the server will test the header first to see weather it has GET or POST method  
the result will be send to the php script then back to the server, then to the user
data will be transefer between python and php using subprocess library and php-cgi executable
the uri of the header set to be as an environment variable to be transfered ro the php-cgi 
also teh content type of the pot (tea or coffee) will be sent through php-cgi as response2

--------
make sure you have both server.py and HTCPCP.php in the same folder 
also, you might need to change the path of the php file in the server script in case it doesnt match the esisting one 
This Script doesnt need any dependencies

To execute the code: 
on terminal: sudo python Server.py 127.0.0.1 8080 
on browser: localhost:80/pot-0/black?cream&sugar

To compile the code:
you have to have python2.7 interpreter 
Use the package manager pip to install requests library
development environments: visual studio
