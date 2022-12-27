# PythonHoneyPot
A Simple Python *honey pot* web server which intercepts *GET* requests and responds with a text stream of messages using *chunked transfer encoding*. The idea behind the honey pot is to lure any malicious bots which could be scraping the site for vulnerabilities. Once the request is estalished - the response starts with an appropriate header and in the body sends infinite UTF-8 encoded text as *chunks* with a delay `SECONDS_PER_MESSAGE` between each chunk - effectively wasting the resources of the connected bot. 

Each text chunk is encoded as follows in the response:
>{*length in bytes of data in hex*}\r\n{*data*}\r\n

This repeats infinitely but could be modified to terminate the connection by sending a 0:
>0\r\n\r\n

The program doesn't use any extra frameworks - only core Python3 libraries. The program was tested using the Python:3.9 environment and the connected clients tested using *curl*, and *Chrome* web browser. The web server uses the base class `ThreadingHTTPServer` to listen for incoming client connections which are then handled by a subclass of `BaseHTTPRequestHandler`. Limitations of the program depend on these python classes and host server hardware. The documentations states that `ThreadingHTTPServer` pre-allocates 100 listening threads to handle incoming client connections and can upscale as necessary. 

### Clone the repository
```
> git clone https://github.com/SethGHall/PythonHoneyPot.git
```

### Running using python: 
Inside the project root folder: Simply run the webserver using the following python command: 
```
> python HoneyPotWebserver.py  
```

Feel free to change the HOSTNAME, PORT, and SECONDS_PER_MESSAGE configurations in the *config.ini* file, otherwise defaults will be supplied by the program. 

Default configuration file contains:
>[DEFAULT]
>HOSTNAME = 0.0.0.0  
>PORT = 8080  
>SECONDS_PER_MESSAGE = 1  

### Running with Docker:
To run the program from within Docker navigate to the root of the project which contains the supplied *DockerFile*. This sets the virtual Python environment to 3.9 and builds the recipe for the image.

To build the Docker image with the tag called *python-honeypot*
```
> docker build -t python-honeypot .
```

To run the container: 
```
> docker run -it -p 8080:8080 python-honeypot 
```
The flag `-it` is set for interactive mode (otherwise use `-d` for detached mode) and port `-p` which maps a container port to a port on the Docker host. By default this is `8080` as specified in the *config.ini* file and with the `EXPOSE` option in the *Dockerfile*. 

I also had this issue https://runnable.com/docker/binding-docker-ports. Docker, by default exposes container to the `ipadress: 0.0.0.0` (unless confilgured otherwise), so I could not just use `localhost`. So make sure the `HOSTNAME=0.0.0.0` is set in the 'config.ini' and using `PORT=8080` to match the docker run command above. This will effectively map `0.0.0.0:8080` from within the container to `localhost:8080` on the external Docker host.

### Client side testing
To test the program as a client, use a browser (tested only with chrome) or curl. 
> http://localhost:8080/
