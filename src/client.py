# -*- coding: utf-8 -*-
import socket as sk

class UDP_Client:
    __COMMAND_LIST='list'
    __COMMAND_GET='get'
    __COMMAND_PUT='put'
    __COMMAND_HELP='help'
    __COMMAND_QUIT='quit'
    
    __connection_port=0
    __connection_address=0
    __buff_size=0
    __stop_connection=False
    #get nome file con gestione errore
    #put nome file, con ricezione risposta
    
    def __init__(self, connection_address, connection_port):
        self.__connection_address=connection_address
        self.__connection_port=connection_port
        self.__buff_size=4096
    
    def __receiveMessage(self, sock):
        data, address=sock.recvfrom(self.__buff_size)
        numPac=int(data.decode('utf8'))
        res=''
        for i in range(numPac):
            data, address=sock.recvfrom(self.__buff_size)
            res=res+data.decode('utf8')
        return res
    
    def __list(self, sock):
        message='list'
        sock.sendto(message.encode('utf8'),(self.__connection_address, self.__connection_port))
        a=self.__receiveMessage(sock)
        print(a)
            
    def run(self):
        print("Trying to connect to %s:%d" % (self.__connection_address, self.__connection_port))
        sock=sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        
        message="Hello"
        sock.sendto(message.encode('utf8'),(self.__connection_address, self.__connection_port))
        
        while not self.__stop_connection:
            text=input('> ')
            command=text.split(' ')[0].lower()
            if command.__eq__(self.__COMMAND_LIST):
                self.__list(sock)
            elif command.__eq__(self.__COMMAND_GET):
                print('GET')
            elif command.__eq__(self.__COMMAND_PUT):
                print('PUT')
            elif command.__eq__(self.__COMMAND_QUIT):
                self.__stop_connection=True
            elif command.__eq__(self.__COMMAND_HELP):
                print('list')
                print('Show avaiable files on server.\n')  
                print('get [file_name]')
                print('Download a file from server.\n')
                print('put [file_name]')
                print('Upload a file to server.\n')
                print('quit')
                print('Shutdown client and close connection.\n')
            else:
                print('Command not found. Try \'help\'')
        
        print('Closing socket connection')
        sock.close()
        print('Client shutting down')
        

c= UDP_Client('localhost', 10000)
c.run()