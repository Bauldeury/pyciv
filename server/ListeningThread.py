import threading

class ListeningThread(threading.Thread):
    
    def __init__(self,server):
        threading.Thread.__init__(self)
        self.server = server

    
    def run(self):
        while self.server.listening:
            self.server.sock.listen(5)
            (conn, (c_ip, c_port)) = self.server.sock.accept()
            self.server.createConnectionThread(conn, c_ip, c_port)
            
        self.server.stop()