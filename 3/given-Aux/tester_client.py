import socket


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8000)
sock.connect(server_address)
try:
    message = '[1,2]\ntrue\n[3,4]'
    # Send data
    sock.sendall(bytearray(message, 'utf-8'))
    # Receive data
    output = ''
    while True:
        data = sock.recv(16)
        output += data.decode('utf-8')
        if len(data) < 16:
            print(output, end='')
            break
finally:
    sock.close()