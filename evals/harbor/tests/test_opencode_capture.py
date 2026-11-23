"""Behavior checks for OpenCode capture's server and invocation gates."""
import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'plugins/agentic-devcraft/skills/capture-agent-issue/scripts/opencode_capture.py'
spec = importlib.util.spec_from_file_location('opencode_capture', SOURCE)
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class OpenCodeCaptureTests(unittest.TestCase):
    session_id = 'ses_test1'
    session_route = f'/api/session/{session_id}'
    user_route = f'{session_route}/message?order=desc&limit=1&type=user'
    session = {'data': {'id': session_id, 'location': {'directory': '/test/project'},
                        'time': {'created': 1}}}
    invocation = {'id': 'msg_invocation', 'type': 'user', 'text': '$capture-agent-issue synthetic'}

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.registry = Path(temp.name)
        for pid, port in [(200, 41200), (300, 41300)]:
            (self.registry / f'{pid}.json').write_text(json.dumps({
                'pid': pid, 'port': port, 'binary': '/test/opencode',
            }))
        self.env = {'OPENCODE_CLIENT': 'openchamber', 'OPENCODE_SESSION_ID': self.session_id,
                    'OPENCHAMBER_MANAGED_PROCESS_REGISTRY': str(self.registry)}

    def launch(self, responses):
        def get(binary, server, env, route):
            return responses[server, route]

        with patch.dict(capture.os.environ, self.env, clear=True), \
                patch.object(capture, 'ancestry', return_value=[100, 200, 150]), \
                patch.object(capture, 'get', side_effect=get):
            return capture.capture(argparse.Namespace(action='launch'))

    def test_launcher_reads_wrapped_records_from_the_shells_server(self):
        server = 'http://127.0.0.1:41200'
        result = self.launch({
            (server, '/api/info'): {'pid': 200, 'version': '2.3.2'},
            (server, self.session_route): self.session,
            (server, self.user_route): {'data': [self.invocation]},
        })
        self.assertEqual(result['mode'], 'ordinary')
        self.assertEqual(result['directory'], '/test/project')
        self.assertEqual(result['invocation'], {
            'id': 'msg_invocation', 'text': '$capture-agent-issue synthetic',
        })

    def test_non_owning_process_is_rejected_even_if_it_can_serve_the_session(self):
        server = 'http://127.0.0.1:41300'
        self.env['CAPTURE_OPENCODE_SERVER'] = server
        self.env['OPENCODE_BINARY'] = '/test/opencode'
        with self.assertRaisesRegex(ValueError, 'not the server that owns'):
            self.launch({
                (server, '/api/info'): {'pid': 300, 'version': '2.3.2'},
                (server, self.session_route): self.session,
                (server, self.user_route): {'data': [self.invocation]},
            })

    def test_newest_message_without_a_user_boundary_is_not_an_empty_capture(self):
        server = 'http://127.0.0.1:41200'
        with self.assertRaisesRegex(ValueError, 'invocation boundary'):
            self.launch({
                (server, '/api/info'): {'pid': 200, 'version': '2.3.2'},
                (server, self.session_route): self.session,
                (server, self.user_route): {'data': []},
            })

    def test_normal_cli_uses_its_own_registered_service(self):
        server = 'http://127.0.0.1:41200'
        (self.registry / 'opencode').mkdir()
        (self.registry / 'opencode/service.json').write_text(json.dumps({
            'pid': 200, 'url': server,
        }))
        self.env.update(OPENCODE_CLIENT='cli', XDG_STATE_HOME=str(self.registry),
                        OPENCODE_BINARY='/test/opencode')
        result = self.launch({
            (server, '/api/info'): {'pid': 200, 'version': '2.3.2'},
            (server, self.session_route): self.session,
            (server, self.user_route): {'data': [self.invocation]},
        })
        self.assertEqual(result['server_pid'], 200)
