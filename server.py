import socket, threading, os, time, datetime

def get_file(path):
    content = None
    try:
        f = open(path, "rb")
        content = f.read()
        f.close()
    except IOError:
        content = None
    finally:
        return content

bind_ip = '127.0.0.1'
bind_port = 5742

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(10)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


# Errors
codes = {
    "ok": "00",
    IOError: "60",
}

# Data types
# types = {
#     0: get.get_text_file,
#     1: get.get_binary_file
# }

def handle_request(request, client_socket, address):

    request_arr = request.split(' ')
    
    try:
            
            # content = types.get(int(request_arr[1]))(request_arr[0][1:])
            content = get_file(request_arr[0][1:])
            if not content:
                raise IOError
            else:
                client_socket.sendall(content)
            status_code = codes.get("ok")
        
    except IOError:
        
        status_code = str(codes.get(IOError))
        
        # print(f"\033[1;31mError!\033[0m {e}")
        # print(f"Sending status code {status_code} to client.")
        
        client_socket.send(status_code.encode())

    print("[{}] ".format(datetime.datetime.fromtimestamp(time.time())), end = "")

    if status_code == codes.get("ok"): 
        print("\33[32m", end = "")
    elif status_code == codes.get(IOError): 
        print("\33[33m", end = "")
    print("{}:{} [{}]: {}\33[0m".format(address[0], address[1], status_code, request_arr[0]))
    
    
def handle_client_connection(client_socket, address):
    
    request = client_socket.recv(1024)
    # print('Received "{}"'.format(request.decode()))
    
    handle_request(request.decode(), client_socket, address)
    client_socket.close()

while True:
    try:
        client_sock, address = server.accept()
        # print('Accepted connection from {}:{}'.format(address[0], address[1]))
    
        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock, address))
        client_handler.start()
    except (KeyboardInterrupt, EOFError):
        print("Closing server")
        server.close()
