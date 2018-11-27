import socket
import json

class ClientMessager:
    def __init__(self, hostname, port):
        """ Create a connection to the server..
        :param String hostname: the name of the host
        :param nat port: port number to connect to
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((hostname, port))

    def receive_message(self):
        """
        :rtype Json: the message received
        """
        message = self._socket.recv(4096).decode()
        print("recv message", message)
        return json.loads(message)

    def send_register_message(self, name):
        """
        :param String name: name that player has chosen
        """
        self._socket.send(json.dumps(name).encode())

    def respond_placement_message(self, placement):
        """
        :param (Worker, (row, col)) placement: the placement that was
                                               chosen
        :param String name: the name of the player
        """
        _, coordinate = placement
        self._socket.send(json.dumps(coordinate).encode())

    def respond_turn_message(self, turn, name):
        """
        :param (Worker, Direction, Direction) turn:
        :param String name: the name of the player
        """
        if all(element is None for element in turn):
            action = json.dumps(name).encode()
        elif turn[2] is None:
            action = ([turn[0]] + turn[1].string_values())
        else:
            action = ([turn[0]] + turn[1].string_values()
                      + turn[2].string_values())
        self._socket.send(json.dumps(action).encode())
