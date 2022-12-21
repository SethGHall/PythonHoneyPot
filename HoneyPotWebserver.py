#   Honey Pot Web Server - A basic implementation which intercepts all GET requests and
#   sends an infinite stream of text data to an HTTP client program or browser. The port,
#   hostname and seconds between each line of text data can be overridden in the config.ini 
#   configuration file.
#
#   Author: Seth Hall
#   Date: 21 December 2022
import configparser as config
import http.server as server
import socketserver as socket
from functools import partial
import time as time

#Honey Pot web handler - subclass of BaseHTTPRequest Handler - an instance of this handler is created
#to handle each individual HTTP client request - connection will keep alive until client quits
class HoneyPotHandler(server.BaseHTTPRequestHandler):

    responses = ["...Sorry Not Found...", "Or maybe it is found?...", "Keep waiting and maybe it will come...", 
                "Any second now..", "This is SO NOT a honeypot...", "Alright here it is...", 
                "Almost there...", "Almost...", "keep waiting...", "loading now...", 
                "Such juicy content is on its way...", "you are being so patient...",
                 "Next line, I promise it will be here...","here it is!!!..."]

    def __init__(self, sec_time, request, client_address, server):
        self.sec_time = sec_time
        super().__init__(request, client_address, server)
    
    #Process all HTTP GET operations - have to set protocol to HTTP1.1 to ensure "chunked" data transfew
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        #Set the HTTP Header
        self.send_response(200)
        #had to set event-stream to allow chrome rendering with no buffer
        self.send_header("Content-type","text/event-stream; charset=utf8") 
        self.send_header("Transfer-Encoding","chunked")
        self.end_headers()
        print("Another falls into the trap!")
        #serve infinite text stream for connected client
        self.process_honeypot_GET()

    #Helper method to send chunked text data
    def process_honeypot_GET(self):
        try:
            x = 0;
            #loop rotating text responses from the attribute array
            while True:
                self.REPLY = self.responses[x]+"\n"
                replyLength = len(self.REPLY)
                #Writing protocol for "chunked" data transfer https://en.wikipedia.org/wiki/Chunked_transfer_encoding
                #Follows the pattern length(data)\r\n(data)\r\n where the length is given as a hexidecimal string
                self.wfile.write('{:X}\r\n{}\r\n'.format(replyLength, self.REPLY).encode("utf-8"))
                time.sleep(self.sec_time)
                x = (x+1) % len(self.responses)
            #Code to terminate stream - although will never get to this - but was used for testing 
            self.wfile.write('0\r\n\r\n'.encode('utf-8'))
        except Exception as err:
            #Exception is generated when the client terminates connection
            print("The {} finally gave up! ".format(self.client_address))

#main class used to run the threaded HTTP server sockets - each time a client connects they are  
#processed synchronously and handled with an instance of the HoneyPotHandler
class main:
    #Set some host defaults first
    hostName = "localhost"
    port = 8080
    sec_time = 5
    try:
        #Read config.ini to obtain any custom configurations
        config = config.ConfigParser(delimiters=('=', ':'))
        config.read('config.ini')
        config = config['DEFAULT']
        hostName = config['HOSTNAME'] 
        port = int(config['PORT'])
        sec_time = int(config['SECONDS_PER_MESSAGE'])
    except (KeyError, Exception) as error:
        print("An error occored {} reading config - setting defaults localhost:8080".format(error.message))

    #Need to create a partial to apply sec_time argument before passing to threading server 
    honeypot = partial(HoneyPotHandler, sec_time)
    #Create Threading HTTP Server to handle multi client connections
    server = server.ThreadingHTTPServer((hostName, port), honeypot, sec_time)
    print("Server started on {}:{}".format(hostName,port))
    try:
        #start listening for client connections
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server terminated....")
    #Close the listening server
    server.server_close()

#Call the main class instance
if __name__ == "__main__":
    main()