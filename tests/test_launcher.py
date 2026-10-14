import errno
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from portable import server


class LauncherTests(unittest.TestCase):
    def test_busy_default_port_moves_and_updates_origin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'index.html').write_text('test')
            addresses = []
            class FakeServer:
                def __init__(self, address, handler):
                    addresses.append(address)
                    if address[1] == 8010: raise OSError(errno.EADDRINUSE, 'busy')
                    self.server_address = address
                def serve_forever(self): pass
                def server_close(self): pass
            argv = ['server.py', '--public', str(root), '--database', str(root / 'accounts.sqlite3')]
            with patch.dict(server.os.environ, {}, clear=True), patch.object(server, 'read_dotenv'), patch.object(server.sys, 'argv', argv), patch.object(server, 'ThreadingHTTPServer', FakeServer), patch.object(server, 'Application', return_value=object()) as application:
                server.main()
                self.assertEqual(addresses, [('127.0.0.1', 8010), ('127.0.0.1', 8011)])
                self.assertEqual(application.call_args.args[2], 'http://127.0.0.1:8011')

    def test_explicit_busy_port_never_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            argv = ['server.py', '--public', directory, '--port', '8010']
            with patch.dict(server.os.environ, {}, clear=True), patch.object(server, 'read_dotenv'), patch.object(server.sys, 'argv', argv), patch.object(server, 'ThreadingHTTPServer', side_effect=OSError(errno.EADDRINUSE, 'busy')) as factory:
                with self.assertRaises(SystemExit): server.main()
                self.assertEqual(factory.call_count, 1)
