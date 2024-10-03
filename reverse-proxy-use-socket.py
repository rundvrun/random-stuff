import socket

PROXY_PORT = 8001
SERVICE_PORT = 8000
SERVICE_HOST = '::1'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', PROXY_PORT)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        data = b''
        connection.settimeout(1)
        try:
            while (r := connection.recv(1024)): data += r
        except: pass
        if data:
            print(f'{client_address} connected')
            print('\nREQUEST:\n{!r}\n'.format(data))
            sock_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock_server.connect((SERVICE_HOST, SERVICE_PORT))
            sock_server.sendall(data)
            data_server = b''
            while (rx := sock_server.recv(1024)): data_server += rx
            sock_server.close()
            print('\nRESPONSE:\n{!r}\n'.format(data_server))
            if data_server: connection.sendall(data_server)
    finally: connection.close()
