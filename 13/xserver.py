#!/usr/bin/env python3.6
"""
Runs Santorini tournament(s) with clients over TCP
"""

import sys
import os
import json
import socket
import time
sys.path.append('..')
from Santorini.Admin.tournament_manager import TournamentManager
from Santorini.Remote.remote_proxy_player import RemoteProxyPlayer
from Santorini.Lib.json_validate import validate_json
from Santorini.Remote.jsonschemas import NAME
import socket

tm = TournamentManager()

config = json.loads(sys.stdin.read())

client_sockets = []

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind(('0.0.0.0', config["port"]))

start_time = time.time()

def check_time():
    """
    Checks if the client connection period is over
    and runs a tournament if it isn't

    tournaments are only started if at least the minimum
    amount of players have joined the tournament in the alloted time
    """
    if (time.time() - start_time) >= config["waiting for"]:
        if len(tm.uuids_players) >= config["min players"]:
            nef_players, meet_up_results = tm.run_tournament()
            send_results(nef_players, meet_up_results)
            if config["repeat"] == 1:
                reset()
            else:
                sys.exit(0)
        else:
            raise Exception("not enough clients in tournament")

def reset():
    """
    resets state so another tournament can be played
    """
    global tm, client_sockets, start_time
    tm = TournamentManager()
    client_sockets = []
    start_time = time.time()

def send_results(nef_players, meet_up_results):
    """
    sends the results of a tournament to clients and stdout
    :param List of Str nef_players: list of nefarious players
    :param List of MeetUpResults meet_up_results: list of meet up results
    """
    for meet_up_result in meet_up_results:
        winner, loser = meet_up_result
        if loser in nef_players:
            meet_up_result.append("irregular")

    dumped_results = json.dumps(meet_up_results)

    print(dumped_results)

    for sock in client_sockets:
        try:
            sock.send(dumped_results.encode())
        except:
            pass
        finally:
            sock.close()

stopped = False
while not stopped:
  try:
    tcpServer.settimeout(0.2) # timeout for listening
    tcpServer.listen(1) 
    conn, _ = tcpServer.accept()

    name = json.loads(conn.recv(4096).decode())
    if validate_json(NAME, name):
        client_sockets.append(conn)
        rpp = RemoteProxyPlayer(conn)
        tm._add_player_direct(rpp, name)
  except socket.timeout:
    check_time()
  except:
    raise
