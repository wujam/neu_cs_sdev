#!/usr/bin/env python3.6

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
import json
from Santorini.Common.player_interface import AbstractPlayer
from Santorini.Remote.remote_proxy_server import RemoteProxyServer
from multiprocessing import Process
import importlib
import importlib.util
import inspect
import time

WAIT_BETWEEN_PLAYERS = 1

config = json.loads(sys.stdin.read())

ip = config["ip"]
port = config["port"]

playerconfigs = config["players"]
player_components = []
for player_spec in playerconfigs:
    _, name, path = player_spec
    
    spec = importlib.util.spec_from_file_location("mod", path)
    if spec is None:
        continue
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    found = inspect.getmembers(module,
                               predicate=lambda o: inspect.isclass(o) and \
                                                   issubclass(o, AbstractPlayer) and \
                                                   o != AbstractPlayer)
    player_class = found[0][1]
    player = player_class()
    client_connection = RemoteProxyServer(ip, port, player, name)
    player_components.append(client_connection)

def start_rps(rps):
    """
    Starts a remote proxy server
    :param RemoteProxyServer rps: the server to start
    """
    rps.start()

player_procs = []

for rps in player_components:
    p = Process(target=start_rps, args=[rps])
    player_procs.append(p)
    p.start()
    time.sleep(WAIT_BETWEEN_PLAYERS)

for p in player_procs:
    p.join()
