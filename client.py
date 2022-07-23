# -*- coding: utf-8 -*-
import socket as sk

class UDP_Client:
    __connection_port=0
    __connection_address=0
    def __init__(self, connection_address, connection_port):
        self.__connection_address=connection_address
        self.__connection_port=connection_port
    
    def run(self):
        print("Trying to connect to %s:%d" % (self.__connection_address, self.__connection_port))
        sock=sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        try:
            sock.connect()
        except Exception:
            print("Connection to server failed. Check server socket")
        
        

c= UDP_Client('100.100.100.100', 60)
c.run()