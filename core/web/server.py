import socket
import threading


class Server:
    def __init__(self, ip='127.0.0.1', port=20070, max_data=1024, username='vv'):
        self.conn = None
        self.addr = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.server.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        self.status = 'close'
        self.ip = ip
        self.port = port
        self.max_data = max_data
        self.datas = {'msg': []}
        self.username = username

    def get_from_client(self):
        pass

    def run_old(self):
        self.status = 'running'
        ip_port = (self.ip, self.port)
        self.server.bind(ip_port)
        self.server.listen(3)
        self.conn, self.addr = self.server.accept()
        while self.status != 'close':
            data = self.get_msg()
            print('Client: ' + data)
            message = input("SERVER >")
            self.send_msg(message)
            print(self.datas)
            if message == '//c':
                self.status = 'close'

    def run(self):
        self.status = 'running'
        ip_port = (self.ip, self.port)
        self.server.bind(ip_port)
        self.server.listen(3)
        self.conn, self.addr = self.server.accept()
        print(self.addr)

    def send_msg(self, msg):
        self.datas['msg'].append({'text': msg.encode('utf-8'), 'user': self.username})
        self.conn.send(msg.encode('utf-8'))

    def get_msg(self):
        msg = self.conn.recv(self.max_data).decode('utf-8')
        self.datas['msg'].append({'text': msg.encode('utf-8'), 'user': self.username})
        return msg

    def listen_msg(self):
        self.status = 'running'

        def listen_thread():
            while True:
                msg = self.get_msg()
                self.datas['msg'].append({'text': msg, 'user': self.username})
                if msg == '':
                    continue
                print('Client: ' + msg)

        listener = threading.Thread(target=listen_thread)
        listener.setDaemon(True)
        listener.start()


if __name__ == '__main__':
    s = Server()

    s.run()
    s.listen_msg()
    while True:
        if s.status != 'running':
            break
