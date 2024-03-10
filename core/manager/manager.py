from core.web import server, client


def start(ip='127.0.0.1', port=20070):
    sev = server.Server(ip, port)
    sev.run()
    sev.listen_msg()
    cli = client.Client()
    cli.wait()
    while True:
        if sev.status != 'running':
            break


if __name__ == '__main__':
    start()
