import socket


class Client:
    def __init__(self, ip='127.0.0.1', port=20070, max_data=1024, username='nn'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        self.status = 'close'
        self.ip = ip
        self.port = port
        self.max_data = max_data
        self.username = username
        self.datas = {'msg': []}

    def wait(self):
        self.ip = None
        self.port = None
        self.max_data = None
        self.status = 'waiting'

    def run_old(self):
        self.status = 'running'
        ip_port = (self.ip, self.port)
        self.client.connect(ip_port)
        while self.status != 'close':
            message = input('CLIENT >')
            self.send_msg(message)
            # server_msg = self.get_msg()
            # print('Server: ' + server_msg)
            # print(self.datas)
            # if server_msg == '//c':
            #     self.status = 'close'

    def run(self):
        self.status = 'running'
        ip_port = (self.ip, self.port)
        self.client.connect(ip_port)

    def send_msg(self, msg):
        self.datas['msg'].append({'text': msg.encode('utf-8'), 'user': self.username})
        self.client.send(msg.encode('utf-8'))

    def get_msg(self):
        msg = self.client.recv(self.max_data).decode('utf-8')
        self.datas['msg'].append({'text': msg.encode('utf-8'), 'user': self.username})
        return msg


if __name__ == '__main__':
    c = Client()
    c.run_old()
