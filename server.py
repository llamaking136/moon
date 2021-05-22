import socket
import threading
import os
import getters as get

bind_ip = '127.0.0.1'
bind_port = 5742

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(10)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


# Errors
codes = {
    IOError: 60,
}

# Data types
types = {
    0: get.get_text_file,
    1: get.get_binary_file
}

def handle_request(request, client_socket):

    request_arr = request.split(' ')
    
    try:
            content = types.get(int(request_arr[1]))(request_arr[0][1:])
            client_socket.sendall(content)
        
    except IOError as e:
        
        status_code = str(codes.get(IOError))
        
        print(f"\033[1;31mError!\033[0m {e}")
        print(f"Sending status code {status_code} to client.")
        
        client_socket.send(status_code.encode())
    
    
def handle_client_connection(client_socket):
    
    request = client_socket.recv(1024)
    print('Received "{}"'.format(request.decode()))
    
    handle_request(request.decode(), client_socket)
    client_socket.close()

while True:
    
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    
    client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,))
    client_handler.start()
