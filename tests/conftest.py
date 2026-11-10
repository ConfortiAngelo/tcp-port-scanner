import socket
import socketserver
import threading

import pytest


@pytest.fixture(autouse=True)
def _isolate_logs(tmp_path, monkeypatch):
    # The logger writes to app/logs relative to the working directory.
    monkeypatch.chdir(tmp_path)


class _BannerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"SSH-2.0-OpenSSH_9.6\r\n")


@pytest.fixture
def ssh_like_server():
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _BannerHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server.server_address[1]
    server.shutdown()
    server.server_close()


@pytest.fixture
def closed_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
