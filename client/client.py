import socket
import select

from .RootPanel import RootPanel
from .DataSynchroniser import DataSynchroniser


class Client:
    def __init__(self):
        self.pMain = RootPanel(self)
        self.pMain.protocol("WM_DELETE_WINDOW", self.stop)
        self.dataSynchroniser = DataSynchroniser(self)

        self._connect()

    def _connect(self):
        self.hote = "localhost"
        self.port = 6951

        self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssocket.connect((self.hote, self.port))
        print("[+] Connection on {}:{}.".format(self.hote, self.port))

    def stop(self):
        self.quitflag = True
        self.ssocket.close()
        print("[-] Connection closed.")

    def start(self):
        self.quitflag = False

        buffer = b""
        while True:
            self.pMain.update()
            if self.quitflag:
                break

            # self.ssocket.setblocking(0)
            rsock, wsock, esock = select.select([self.ssocket], [], [], 0.02)
            for sock in rsock:
                response = sock.recv(256)
                if response != b"":
                    buffer = buffer + response
                    if buffer[-1] == 4:  # EOT ASCII CHAR
                        self.executeInfo(buffer)
                        buffer = b""
                else:
                    print("clean disconnect [type 1]")
                    break

    def executeInfo(self, encoded_info:bytes):
        """from CONNECTIONTHREAD(server) to CLIENT"""

        print("SERVER >> {}".format(encoded_info))
        info = encoded_info.decode()[:-1]

        self.dataSynchroniser.executeInfo(info)
        self.pMain.executeInfo(info)

    def executeCmd(self, cmd:str):
        """from UI to CLIENT"""
        if cmd == "quit":
            self.stop()
        else:
            self._sendCmd(cmd)

    def _sendCmd(self, cmd:str):
        """from CLIENT to CONNECTION THREAD(server)"""
        encoded_cmd = cmd.encode() + b"\x04"
        print("SERVER << {}".format(encoded_cmd))
        self.ssocket.send(encoded_cmd)


def main():
    app = Client()
    app.start()


if __name__ == "__main__":
    main()
