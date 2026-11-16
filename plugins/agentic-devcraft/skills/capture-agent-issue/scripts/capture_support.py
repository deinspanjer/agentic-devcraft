#!/usr/bin/env python3
"""Read scoped transcript metrics, or exclusively save prepared Markdown. Stdlib only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp needs an explicit timezone')
    return result.astimezone(timezone.utc)


def snapshot(args):
    """Return only the requested physical prefix; fail on an unresolvable boundary."""
    selected = []
    end = 0
    found = False
    with Path(args.transcript).open('rb') as source:
        for number, raw in enumerate(source, 1):
            next_end = end + len(raw)
            if args.end_byte_exclusive is not None and next_end > args.end_byte_exclusive:
                raise ValueError('Byte cutoff must end on a JSONL record boundary')
            row = json.loads(raw)
            ordinal = row.get('ordinal')
            if args.end_ordinal_exclusive is not None:
                if not isinstance(ordinal, int):
                    raise ValueError('Ordinal cutoff needs recorded ordinals')
                if ordinal >= args.end_ordinal_exclusive:
                    found = True
                    break
            if args.before is not None and row.get('timestamp'):
                if instant(row['timestamp']) >= instant(args.before):
                    found = True
                    break
            selected.append((number, row))
            end = next_end
            if ((args.end_byte_exclusive is not None and end == args.end_byte_exclusive)
                or (args.end_line_inclusive is not None and number == args.end_line_inclusive)
                or (args.through_uuid is not None and row.get('uuid') == args.through_uuid)):
                found = True
                break
    if args.end_ordinal_exclusive is not None and selected:
        found = found or selected[-1][1].get('ordinal') == args.end_ordinal_exclusive - 1
    if args.before is not None:
        # The explicit time selects all earlier recorded events even if EOF is earlier.
        found = True
    if not found or not selected:
        raise ValueError('Cutoff did not resolve to a nonempty source prefix')
    return selected, end


def origin_kind(row):
    origin = row.get('origin') or {}
    return origin.get('kind') or row.get('origin_kind')


def metrics(args):
    selected, size = snapshot(args)
    turns, peers, unknown, tools, seen = set(), set(), set(), set(), set()
    runtime, changes = {}, []
    first = last = None
    start = None
    start_line = None
    matched = False
    title = cwd = None
    latest_usage = None
    cumulative = None
    canonical_users = any(r.get('type') == 'event_msg' and
                          r.get('payload', {}).get('type') == 'user_message'
                          for _, r in selected)

    def put(key, value, line, method='recorded'):
        if value is not None:
            runtime[key] = {'value': value, 'source_line': line, 'method': method}

    for line, row in selected:
        kind = row.get('type')
        payload = row.get('payload') or {}
        row_sid = row.get('sessionId')
        if args.harness == 'claude' and row_sid != args.subject_id:
            continue
        if args.harness == 'codex' and kind == 'session_meta':
            sid = payload.get('id') or payload.get('session_id')
            if sid != args.subject_id:
                raise ValueError('Source session metadata does not match subject ID')
            matched = True
            start = payload.get('timestamp') or row.get('timestamp')
            start_line = line
            put('harness_version', payload.get('cli_version'), line)
            cwd = payload.get('cwd')
        if args.harness == 'claude':
            matched = True
        if row.get('timestamp'):
            first = first or row['timestamp']
            last = row['timestamp']
        identity = row.get('uuid')
        if identity and identity in seen:
            continue
        if identity:
            seen.add(identity)
        if args.harness == 'codex':
            if kind == 'turn_context':
                for key in ('model', 'effort'):
                    put(key, payload.get(key), line)
                cwd = payload.get('cwd') or cwd
            if kind == 'event_msg' and payload.get('type') == 'token_count':
                info = payload.get('info') or {}
                usage = info.get('last_token_usage') or {}
                put('context_capacity', info.get('model_context_window'), line)
                put('context_used', usage.get('total_tokens'), line,
                    'latest reported request total (input plus output); not instantaneous')
                cumulative = info.get('total_token_usage') or cumulative
                latest_usage = usage or latest_usage
            if kind == 'response_item' and payload.get('type') in ('function_call', 'custom_tool_call'):
                if payload.get('call_id'):
                    tools.add(payload['call_id'])
            is_event = kind == 'event_msg' and payload.get('type') == 'user_message'
            is_message = kind == 'response_item' and payload.get('type') == 'message' and payload.get('role') == 'user'
            if is_event or (is_message and not canonical_users):
                meta = row.get('metadata') or {}
                retained_id = (meta.get('retained_source') or {}).get('id') or {}
                uid = retained_id.get('message_id') or payload.get('id') or f'line:{line}'
                provenance = payload.get('internal_chat_message_metadata_passthrough') or {}
                kinds = provenance.get('content_item_kinds') or []
                origin = origin_kind(row) or origin_kind(payload)
                if origin in ('peer', 'agent'):
                    peers.add(uid)
                elif origin == 'human' or (origin is None and (is_event or 'user.text' in kinds)):
                    turns.add(uid)
                elif origin is None and kinds:
                    pass  # Native instruction/attachment content is not human input.
                else:
                    unknown.add(uid)
        else:
            cwd = row.get('cwd') or cwd
            if kind == 'custom-title':
                title = row.get('customTitle')
            if kind == 'user':
                content = row.get('message', {}).get('content', [])
                tool_result = isinstance(content, list) and any(
                    isinstance(c, dict) and c.get('type') == 'tool_result' for c in content)
                uid = identity or f'line:{line}'
                origin = origin_kind(row)
                if origin == 'peer':
                    peers.add(uid)
                elif not (tool_result or row.get('isMeta') or row.get('isCompactSummary')):
                    if origin == 'human':
                        turns.add(uid)
                    else:
                        unknown.add(uid)
            if kind == 'api-request':
                params = row.get('params') or {}
                put('effort', (params.get('output_config') or {}).get('effort'), line)
                capacity = params.get('context_window_size')
                put('context_capacity', capacity, line)
            if kind == 'assistant':
                message = row.get('message') or {}
                put('harness_version', row.get('version'), line)
                put('model', message.get('model'), line)
                put('effort', row.get('perTurnEffort') or row.get('effort'), line)
                usage = message.get('usage')
                if usage:
                    latest_usage = usage
                    keys = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
                    if all(isinstance(usage.get(k, 0), (int, float)) for k in keys):
                        put('context_used', sum(usage.get(k, 0) for k in keys), line,
                            'latest reported response input + cache-creation + cache-read input')
                for c in message.get('content', []):
                    if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('id'):
                        tools.add(c['id'])
        setting = tuple(runtime.get(k, {}).get('value') for k in ('model', 'effort'))
        if any(v is not None for v in setting) and (not changes or changes[-1]['settings'] != list(setting)):
            changes.append({'source_line': line, 'settings': list(setting)})
    if not matched:
        raise ValueError('Subject ID was not found in source records')
    missing = {'value': None, 'status': 'unavailable', 'reason': 'not exposed in selected source records'}
    for field in ('harness_version', 'model', 'effort', 'context_used', 'context_capacity'):
        runtime.setdefault(field, dict(missing))
    observed_start = start or first
    as_of = args.before or last
    age = (instant(as_of) - instant(observed_start)).total_seconds() if observed_start and as_of else None
    boundary = {k: getattr(args, k) for k in (
        'end_ordinal_exclusive', 'end_byte_exclusive', 'end_line_inclusive', 'through_uuid', 'before')
        if getattr(args, k) is not None}
    return {'schema': 'agent-issue-metrics/v1', 'harness': args.harness,
            'subject_id': args.subject_id, 'source': str(Path(args.transcript).resolve()),
            'cutoff': boundary, 'as_of': as_of, 'subject_project_cwd': cwd, 'subject_title': title,
            'runtime': runtime, 'runtime_changes': changes,
            'session': {'start': observed_start, 'start_source_line': start_line,
                        'age_seconds': age, 'age_is_lower_bound': start is None,
                        'transcript_kb': size / 1000, 'physical_prefix_bytes': size,
                        'source_records_in_prefix': len(selected), 'human_turns': len(turns),
                        'peer_requests': len(peers), 'unknown_origin_messages': len(unknown),
                        'tool_invocations': len(tools)},
            'accounting': {'turns': 'human-origin user messages; canonical native user events or user.text provenance in Codex; tool results and generated attachments excluded',
                           'tools': 'unique invocation IDs, not results or repeated blocks',
                           'size': 'physical original-file prefix, decimal KB; includes metadata',
                           'scope': 'subject ID only for Claude; original source prefix for Codex'},
            'latest_reported_usage': latest_usage, 'cumulative_usage': cumulative}


def component(name, fallback, parent):
    name = name or fallback
    forbidden = r'[\x00/]' if os.name != 'nt' else r'[\x00-\x1f<>:"/\\|?*]'
    result = re.sub(forbidden, ' - ', name)
    if result in ('.', '..') or not result:
        result = fallback
    if os.name == 'nt':
        result = result.rstrip(' .') or fallback
        if result.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1,10)), *('LPT'+str(i) for i in range(1,10))}:
            result += ' - name'
    limit = os.pathconf(parent, 'PC_NAME_MAX') if hasattr(os, 'pathconf') else 255
    if limit > 0 and len(os.fsencode(result)) > limit:
        suffix = '-' + hashlib.sha256(name.encode()).hexdigest()[:10]
        while len(os.fsencode(result + suffix)) > limit:
            result = result[:-1]
        result += suffix
    return result


def private_directory(path):
    # Refuse symlinks in the generated temp subtree instead of following a planted name.
    if path.is_symlink():
        raise ValueError(f'Refusing generated directory symlink: {path}')
    path.mkdir(mode=0o700, exist_ok=True)
    if not path.is_dir() or (hasattr(os, 'getuid') and path.stat().st_uid != os.getuid()):
        raise ValueError(f'Generated directory is not owned by this user: {path}')
    path.chmod(0o700)


def save(args):
    body = sys.stdin.buffer.read()
    if not body.strip():
        raise ValueError('Packet Markdown is empty')
    captured = instant(args.captured_at)
    if args.output:
        target = Path(args.output).expanduser().absolute()
        if not target.parent.is_dir():
            raise ValueError('Explicit destination parent must already exist')
    else:
        root = Path(tempfile.gettempdir()).resolve()
        excluded = [Path(p).expanduser().resolve() for p in args.outside]

        def check_location(path):
            if any(path.resolve().is_relative_to(p) for p in excluded):
                raise ValueError('Default temp destination lies inside a supplied worktree')

        check_location(root)
        base = root / 'agent-issues'
        check_location(base)
        private_directory(base)
        project = base / component(args.project, 'unknown-project', base)
        check_location(project)
        private_directory(project)
        session = project / component(args.session, 'untitled-session', project)
        check_location(session)
        private_directory(session)
        leaf = Path(tempfile.mkdtemp(prefix=captured.strftime('%Y-%m-%dT%H-%MZ')+'-', dir=session))
        leaf.chmod(0o700)
        target = leaf / 'packet.md'
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(body)
    digest = hashlib.sha256(body).hexdigest()
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise RuntimeError('Saved packet failed readback verification')
    return {'status': 'complete', 'path': str(target), 'sha256': digest,
            'captured_at_utc': captured.isoformat(), 'bytes': len(body)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    m = sub.add_parser('metrics', help='Read a subject source prefix; emit no conversation text')
    m.add_argument('--harness', choices=('codex', 'claude'), required=True)
    m.add_argument('--transcript', required=True)
    m.add_argument('--subject-id', required=True)
    cut = m.add_mutually_exclusive_group(required=True)
    for flag in ('end-ordinal-exclusive', 'end-byte-exclusive', 'end-line-inclusive'):
        cut.add_argument('--'+flag, type=int)
    cut.add_argument('--through-uuid')
    cut.add_argument('--before')
    s = sub.add_parser('save', help='Save reviewed Markdown from stdin, without overwrite')
    s.add_argument('--project', default='unknown-project')
    s.add_argument('--session', default='untitled-session')
    s.add_argument('--captured-at', required=True)
    s.add_argument('--outside', action='append', default=[])
    s.add_argument('--output')
    args = parser.parse_args()
    try:
        result = metrics(args) if args.command == 'metrics' else save(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc),
                          'intended_output': getattr(args, 'output', None)}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
