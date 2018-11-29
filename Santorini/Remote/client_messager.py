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
        recieves a message from the server
        :rtype Json: the message received
        """
        message = self._socket.recv(4096).decode()
        return json.loads(message)

    def send_register_message(self, name):
        """
        sends a registration message to the server
        :param String name: name that player has chosen
        """
        self._socket.send(json.dumps(name).encode())

    def respond_placement_message(self, placement):
        """
        sends a place to the server
        :param (Worker, (row, col)) placement: the placement that was chosen
        :param String name: the name of the player
        """
        _, coordinate = placement
        self._socket.send(json.dumps(coordinate).encode())

    def respond_turn_message(self, turn, player_uuid, uuid_to_name):
        """
        sends a turn message to the server
        :param (Worker, Direction, Direction) turn:
        :param String name: the name of the player
        """
        if all(element is None for element in turn):
            action = uuid_to_name[player_uuid]
        else:
            worker, move_dir, build_dir = turn
            action = [worker.dump_with_name(uuid_to_name)] + move_dir.string_values()
            if build_dir is not None:
                action += turn[2].string_values()
        self._socket.send(json.dumps(action).encode())
