import socket
import select
import struct
from threading import Thread

# --- CONFIGURATION ---
HOST = '0.0.0.0'
PORT = 1080
USERNAME = "myuser"  # Change this
PASSWORD = "mypassword"  # Change this


# ---------------------

class AuthenticatedSocks5:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def handle_client(self, connection):
        try:
            # 1. Initial Handshake
            # Client sends supported methods
            data = connection.recv(2)
            if not data: return
            version, nmethods = struct.unpack("!BB", data)
            methods = connection.recv(nmethods)

            # Tell client we REQUIRE Username/Password (0x02)
            connection.sendall(struct.pack("!BB", 0x05, 0x02))

            # 2. Authenticate
            auth_version = connection.recv(1)[0]  # Should be 0x01
            un_len = connection.recv(1)[0]
            username = connection.recv(un_len).decode()
            pw_len = connection.recv(1)[0]
            password = connection.recv(pw_len).decode()

            if username == USERNAME and password == PASSWORD:
                print('Authentication!')
                connection.sendall(struct.pack("!BB", 0x01, 0x00))  # Success
            else:
                print('Authentication FAILED!')
                connection.sendall(struct.pack("!BB", 0x01, 0x01))  # Failure
                return

            # 3. Request details (where Telegram wants to go)
            data = connection.recv(4)
            if not data: return
            version, cmd, _, address_type = struct.unpack("!BBBB", data)

            if address_type == 1:  # IPv4
                address = socket.inet_ntoa(connection.recv(4))
            elif address_type == 3:  # Domain name
                domain_length = connection.recv(1)[0]
                address = connection.recv(domain_length).decode()
            else:
                return  # IPv6 or other types not handled in this snippet

            port = struct.unpack("!H", connection.recv(2))[0]

            # 4. Connect to destination (Telegram server)
            remote = socket.create_connection((address, port), timeout=10)
            bind_address = remote.getsockname()

            # 5. Reply to client that we are connected
            addr_bytes = socket.inet_aton(bind_address[0])
            reply = struct.pack("!BBBBIH", 0x05, 0x00, 0x00, 0x01,
                                struct.unpack("!I", addr_bytes)[0], bind_address[1])
            connection.sendall(reply)

            # 6. Start data transfer
            self.exchange_data(connection, remote)
        except Exception as e:
            pass  # Connection dropped or timed out
        finally:
            connection.close()

    def exchange_data(self, client, remote):
        inputs = [client, remote]
        while True:
            readable, _, _ = select.select(inputs, [], [], 60)
            if not readable: break  # Timeout
            for s in readable:
                data = s.recv(8192)
                if not data: return
                out = remote if s is client else client
                out.sendall(data)

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(100)
        print(f"SOCKS5 Proxy (Auth Required) on {self.host}:{self.port}")
        while True:
            conn, addr = s.accept()
            Thread(target=self.handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    server = AuthenticatedSocks5(HOST, PORT)
    server.start()