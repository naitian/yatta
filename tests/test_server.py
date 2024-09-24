"""Unit tests for the server module."""

from yatta.web import Server


def test_server_init(app):
    server = Server(app, port=5000)
    assert server.port == 5000
    assert len(server.yatta.dataset) == 5
