# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import socket as sk
import time

class UDP_Server:
    __COMMAND_LIST='list'
    __COMMAND_GET='get'
    __COMMAND_PUT='put'
    __RES_DIR=join('..', 'res', 'server')
    __SENDING_TIME_OUT=0.1
    
    __port=0
    __address=0
    __buff_size=0
    
    def __init__(self):
        self.__address='localhost'
        self.__port=10000
        self.__buff_size=4096
    
    def __createPackages(self, message):
        res=[]
        it=round((len(message)/self.__buff_size)+1)
        e=self.__buff_size
        
        for i in range(it):
            res.append(message[i*self.__buff_size:e])
            e=e+self.__buff_size 
            
        return res
        
        
    def __list(self, sock, address):
        message='2000'
        for f in listdir(self.__RES_DIR):
            if isfile(join(self.__RES_DIR,f)):
                message=message+f+'\n'
                
        p=self.__createPackages(message.encode('utf8'))
        sock.sendto(str(len(p)).encode('utf8'),address)
        
        for i in range(len(p)):
            sock.sendto(p[i],address)
            time.sleep(self.__SENDING_TIME_OUT)
    
    def __doesFileExists(self, filename):
        for f in listdir(self.__RES_DIR):
            if isfile(join(self.__RES_DIR,f)) and f.__eq__(filename):
                return True
        return False
         
        
    def __get(self, sock, address, filename):
        message='2000'.encode('utf8')
        print(message)
        if self.__doesFileExists(filename):
           fileContent=''
           try:
               file=open(join(self.__RES_DIR,filename),'rb')
               fileContent=file.read()
           except Exception as e:
               print(e)
           finally:
                file.close()
           print(type(message))
           print(type(fileContent))
           message=b''.join([message,fileContent])
           print('get request: valid')
        else:
           message='1001'.encode('utf8')
           print('get request: not valid')
           
        p=self.__createPackages(message)
        sock.sendto(str(len(p)).encode('utf8'),address)
        
        for i in range(len(p)):
            sock.sendto(p[i],address)
            time.sleep(self.__SENDING_TIME_OUT)
        
            
    def run(self):
        sock=sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        print('Starting server on %s with port %d\n' %(self.__address, self.__port))
        
        #server socket binding
        try:
            sock.bind((self.__address, self.__port))
        except Exception as error:
            print('Unable to start the server')
            print(error)
            return
        
        #client connection management
        try:
            while True:
            
                data, address= sock.recvfrom(self.__buff_size)
                
                command=str(data.decode('utf8')).split(' ')[0].lower()
                if command.__eq__(self.__COMMAND_LIST):
                    print('list request received')
                    self.__list(sock, address)
                    print('list request accomplished\n')
                elif command.__eq__(self.__COMMAND_GET):
                    print('get request received')
                    stringMessage=data.decode('utf8')
                    file=stringMessage[4:len(stringMessage)]
                    self.__get(sock, address, file)
                elif command.__eq__(self.__COMMAND_PUT):
                    print('put request received')
                else:
                    print('Invalid request received\n')
                    sock.sendto("1000".encode('utf8'),address)
        except Exception as e:
            print(e)
        finally:
            sock.close()
            
s=UDP_Server()
s.run()