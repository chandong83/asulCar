import threading
from time import sleep
from socket import *

default_port = 9190

# 버퍼 사이즈
BUFSIZE = 1024

packetQ = []

CONNECTED = 0
DISCONNECTED = 1

# 서버 대기 큐 
QUEUE_LIMIT = 5
class tcpServer(threading.Thread):
    def __init__(self, port = default_port, callbackFunc = None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.alive = True   
        self.port = port    
        self.callbackFunc = callbackFunc
        self.received = ''    
        self.packetQ = []
        self.running = False
        self.start()
        
    
    def close(self):
        print( 'disconnected ')
        self.alive = False
        self.c_sock.close()
        self.s.close()

    def pull(self):
        if len(self.packetQ) > 0:
            return self.packetQ.pop(0)
        else:
            return None

    def run(self):            
            self.s = socket(AF_INET, SOCK_STREAM)    
            self.s.bind(('', self.port))    
            self.s.listen(QUEUE_LIMIT)

            while self.alive:
                print ('waiting for connection');            
                self.c_sock, self.addr = self.s.accept()   

                if self.callbackFunc is not None: 
                    self.callbackFunc(CONNECTED, self.addr);

                self.running = True
                print ('connected from {}:{}'.format(self.addr[0], self.addr[1]));
                while self.running and self.alive:
                    chunk = self.c_sock.recv(BUFSIZE)
                    if len(chunk) == 0:
                        print('read error')
                        self.running = False
                        break   
                        
                    recvStr = str(chunk, encoding='utf-8')
                    self.received += recvStr   
                    while '\n' in self.received:
                        end = self.received.index('\n')                        
                        msg = self.received[:end]
                        self.received = self.received[end+1:]      
                        if '$' in msg:
                            pack = msg.split('$')[1]        
                            #print(pack)   
                            self.packetQ.append(pack)
                    sleep(0.1)                
                if self.callbackFunc is not None: 
                    self.callbackFunc(DISCONNECTED);                    
                self.c_sock.close()


        
        
