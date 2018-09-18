import socket
import sys

import echo_json


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        lines = ''
        # Receive the data in small chunks and process it
        while True:
            data = connection.recv(16)
            if data:
                lines += data.decode('utf-8')
            if len(data) <= 16:
                data = echo_json.process(lines)
                connection.sendall(bytearray(data, 'utf-8'))
                break
    finally:
        # Clean up the connection
        connection.close()