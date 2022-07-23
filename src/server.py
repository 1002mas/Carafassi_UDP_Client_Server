# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import socket as sk

class UDP_Server:
    __COMMAND_LIST='list'
    __COMMAND_GET='get'
    __COMMAND_PUT='put'
    __RES_DIR='../res/'
    
    __port=0
    __address=0
    __buff_size=0
    
    def __init__(self):
        self.__address='localhost'
        self.__port=10000
        self.__buff_size=4096
    
    def run(self):
        sock=sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        print('Starting server on %s with port %d' %(self.__address, self.__port))
        
        #server socket binding
        try:
            sock.bind((self.__address, self.__port))
        except Exception:
            print('Unable to start the server')
        
        #client connection management
        while True:
            data, address= sock.recvfrom(self.__buff_size)
            print("Received: %s" %(data.decode('utf8')))
            
            command=data.split(' ')[0].lower()
            if command.__eq__(self.__COMMAND_LIST):
                print('list request received')
                self.__list(address)
                print('list request accomplished')
            elif command.__eq__(self.__COMMAND_GET):
                print('get request received')
            elif command.__eq__(self.__COMMAND_PUT):
                print('put request received')
            else:
                print('Invalid request received')
        
        def __list(self, sock):
            message='list'
            sock.sendto(message.encode('utf8'),sock)
            
            
s=UDP_Server()
s.run()