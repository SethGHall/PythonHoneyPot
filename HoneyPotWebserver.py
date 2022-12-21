import numpy as np
import http.server as server
import socketserver as socket
import time as time

hostName = "localhost"
port = 8080

class HoneyPotServer(server.BaseHTTPRequestHandler):

    responses = ["Not Found..", "Or maybe it is found?", "keep waiting and maybe it will come...", "Any second now..", "this is so NOT a honeypot..",
                "Alright here it is...", "almost...", "keep waiting..", "next line I promise it will be here...","......."]

    def __init__(self, request, client_address, server):
        self.REPLY = "HELLO WORLD!!!!\n"
        super().__init__(request, client_address, server)

    def do_GET(self):

        self.protocol_version = 'HTTP/1.1'
        print("protocol version ",self.protocol_version)
        self.send_response(200)
        self.send_header("Content-type","text/event-stream; charset=utf8")
        self.send_header("Transfer-Encoding","chunked")
        self.end_headers()
        self.process_honeypot_GET()

    def process_honeypot_GET(self):
        try:
            x = 0;
            while True:
                #self.wfile.write(hex(len(self.REPLY)).encode("utf-8"))
                self.REPLY = self.responses[x]+"\n"
                replyLength = len(self.REPLY)
                print('{:X}\r\n{}\r\n'.format(replyLength, self.REPLY))
                #self.wfile.write(self.REPLY)
                self.wfile.write('{:X}\r\n{}\r\n'.format(replyLength, self.REPLY).encode("utf-8"))
                time.sleep(1)
                x = (x+1) % len(self.responses)
            self.wfile.write('0\r\n\r\n'.encode('utf-8'))
        except Exception as err:
            print("The {} finally gave up! ".format(self.client_address))

class main:
    server = server.ThreadingHTTPServer((hostName,port),HoneyPotServer)
    print("Server started on {}:{}".format(hostName,port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server terminated....")
        pass

    server.server_close()

if __name__ == "__main__":
    main()