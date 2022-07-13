# -*- coding: utf-8 -*-
import socket as sk
from os.path import join

class UDP_Client:
    __COMMAND_LIST='list'
    __COMMAND_GET='get'
    __COMMAND_PUT='put'
    __COMMAND_HELP='help'
    __COMMAND_QUIT='quit'
    __RES_DIR=join('..', 'res', 'client')
    
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
    
    #get all packets and join them in a single message
    def __receiveMessage(self, sock, isUtf8):
        data, address=sock.recvfrom(self.__buff_size)
        numPac=int(data.decode('utf8'))
        res='' if isUtf8 else bytes()
        for i in range(numPac):
            data, address=sock.recvfrom(self.__buff_size)
            if isUtf8:
                res=res+data.decode('utf8')
            else:
                res=b''.join([res,data])
            if numPac>1:
                print('packet %d/%d'%(i+1,numPac))
        return res
    
    #check responde code
    def __isCodeCorrect(self,message):
        numString=message[0:4]
        return int(numString)>=2000
        
    def __list(self, sock):
        message='list'
        sock.sendto(message.encode('utf8'),(self.__connection_address, self.__connection_port))
        a=self.__receiveMessage(sock, True)
        if self.__isCodeCorrect(a):  
            a=a[4:len(a)]
            print(a)
        else:
            print('File list could not be provided')
            
    def __get(self, sock, message):
        sock.sendto(message.encode('utf8'),(self.__connection_address, self.__connection_port))
        a=self.__receiveMessage(sock, False)
        if self.__isCodeCorrect(a[0:4].decode('utf8')):  
            a=a[4:len(a)]
            filename=message[4:len(message)]
            try:
                file=open(join(self.__RES_DIR,filename),'wb')
                file.write(a)
            except Exception as e:
                print(e)
            finally:
                file.close()
        else:
            print('File not found')
            
    def run(self):
        print("Trying to connect to %s:%d\n" % (self.__connection_address, self.__connection_port))
        sock=sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        
        while not self.__stop_connection:
            text=input('> ')
            command=text.split(' ')[0].lower()
            if command.__eq__(self.__COMMAND_LIST):
                self.__list(sock)
            elif command.__eq__(self.__COMMAND_GET):
                self.__get(sock, text)
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