#!/usr/bin/env python3
"""Read OpenCode capture records from the server that owns this shell."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def ancestry():
    result = subprocess.run(['ps', '-ax', '-o', 'pid=,ppid='],
                            check=True, capture_output=True, text=True, timeout=5)
    parents = {int(pid): int(parent) for pid, parent in
               (line.split() for line in result.stdout.splitlines())}
    pid = os.getpid()
    chain = []
    while (pid := parents.get(pid, 0)) > 1 and pid not in chain:
        chain.append(pid)
    return chain


def record(path):
    try:
        value = json.loads(path.read_bytes())
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        raise ValueError('Cannot read the OpenCode server registration') from None
    return object_value(value, 'server registration')


def object_value(value, label):
    if not isinstance(value, dict):
        raise ValueError(f'Unexpected OpenCode {label} shape')
    return value


def connection(chain, env):
    binary = env.get('OPENCODE_BINARY') or shutil.which('opencode')
    server = env.get('CAPTURE_OPENCODE_SERVER')
    expected_pid = None
    if not server and env.get('OPENCODE_CLIENT') == 'openchamber':
        root = Path(env.get('OPENCHAMBER_MANAGED_PROCESS_REGISTRY') or
                    Path.home() / '.config/openchamber/managed-opencode')
        for pid in chain:
            entry = record(root / f'{pid}.json')
            if entry.get('pid') == pid and type(entry.get('port')) is int:
                expected_pid = pid
                server = f"http://127.0.0.1:{entry['port']}"
                binary = entry.get('binary') or binary
                break
    elif not server:
        state = Path(env.get('XDG_STATE_HOME') or Path.home() / '.local/state')
        entry = record(state / 'opencode/service.json')
        if entry.get('pid') in chain:
            expected_pid = entry['pid']
            server = entry.get('url')
            if entry.get('password'):
                env['OPENCODE_PASSWORD'] = entry['password']

    if not isinstance(server, str) or not server:
        raise ValueError('No server registration for this OpenCode shell; provide its '
                         'local endpoint via CAPTURE_OPENCODE_SERVER')
    loopback = re.fullmatch(r'http://(?:127\.0\.0\.1|\[::1\]):([0-9]{1,5})/?', server)
    if not loopback or not 0 < int(loopback[1]) <= 65535:
        raise ValueError('Expected a credential-free loopback OpenCode server URL')
    if not isinstance(binary, str) or not binary:
        raise ValueError('The OpenCode CLI is unavailable')
    return binary, server, expected_pid


def get(binary, server, env, route):
    result = subprocess.run([binary, '--server', server, 'api', 'GET', route],
                            capture_output=True, env=env, timeout=30)
    if result.returncode:
        # CLI diagnostics can contain connection details. Never echo them or the body.
        if b'requires a password' in result.stderr or b'rejected the password' in result.stderr:
            raise ValueError('OpenCode server authentication failed; use the host connection credentials')
        raise ValueError(f'OpenCode {route.split("/")[2]} read failed (exit {result.returncode})')
    try:
        return object_value(json.loads(result.stdout), 'response')
    except ValueError:
        raise ValueError('Unexpected OpenCode API response (expected a JSON object)') from None


def session_route(session_id):
    if not re.fullmatch(r'ses_[A-Za-z0-9]+', session_id or ''):
        raise ValueError('Missing or invalid OpenCode session ID')
    return f'/api/session/{session_id}'


def capture(args):
    env = os.environ.copy()
    session_id = env.get('OPENCODE_SESSION_ID')
    route = session_route(session_id)
    chain = ancestry()
    binary, server, expected_pid = connection(chain, env)

    def read(path):
        return get(binary, server, env, path)

    info = read('/api/info')
    pid = info.get('pid')
    if type(pid) is not int or pid <= 1:
        raise ValueError('OpenCode /api/info response has no valid server PID')
    if pid not in chain or (expected_pid is not None and pid != expected_pid):
        raise ValueError('OpenCode endpoint is not the server that owns this shell')
    session = object_value(read(route).get('data'), 'session record')
    if not isinstance(session.get('id'), str):
        raise ValueError('OpenCode session record has no ID')
    if session.get('id') != session_id:
        raise ValueError('OpenCode session record does not match OPENCODE_SESSION_ID')

    if args.action == 'export':
        session_route(args.subject_id)
        document = read(f'/api/experimental/session/{args.subject_id}/export')
        data = object_value(document.get('data'), 'export')
        if (object_value(data.get('info'), 'export info').get('id') != args.subject_id
                or not isinstance(data.get('messages'), list)):
            raise ValueError('OpenCode export does not match the requested subject')
        return document

    fork = session.get('fork')
    parent = session.get('parentID')
    if fork is not None:
        mode = 'fork'
    elif parent is not None:
        mode = 'worker'
    else:
        mode = 'ordinary'
    result = {'id': session_id, 'mode': mode, 'parentID': parent, 'fork': fork,
              'directory': object_value(session.get('location'), 'location').get('directory'),
              'created_ms': object_value(session.get('time'), 'session time').get('created'),
              'server_version': info.get('version'), 'server_pid': pid}
    if args.action == 'launch' and mode == 'ordinary':
        rows = read(f'{route}/message?order=desc&limit=1&type=user').get('data')
        if (not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict)
                or rows[0].get('type') != 'user' or not rows[0].get('id')
                or not isinstance(rows[0].get('text'), str)):
            raise ValueError('Cannot establish the invocation boundary from the newest user record')
        result['invocation'] = {'id': rows[0]['id'], 'text': rows[0]['text']}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('launch')
    commands.add_parser('identify')
    commands.add_parser('export').add_argument('subject_id')
    try:
        print(json.dumps(capture(parser.parse_args())))
    except ValueError as exc:
        parser.exit(1, f'{exc}\n')
    except (OSError, subprocess.SubprocessError):
        parser.exit(1, 'Cannot inspect the OpenCode shell ancestry or contact its server\n')


if __name__ == '__main__':
    main()
