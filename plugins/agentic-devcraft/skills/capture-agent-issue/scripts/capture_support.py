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


def iso_ms(value):
    return datetime.fromtimestamp(value / 1000, timezone.utc).isoformat().replace('+00:00', 'Z')


def opencode_metrics(args):
    """Measure a native OpenCode session export up to a message boundary.

    Projected messages are mutable: a tool pending at the cutoff can later complete
    inside the same message. Anything recorded after --cutoff-ms is therefore excluded
    even when its message is inside the boundary.
    """
    document = json.loads(Path(args.transcript).read_bytes())
    data = document.get('data') if isinstance(document, dict) else None
    info = (data or {}).get('info') if isinstance(data, dict) else None
    messages = (data or {}).get('messages') if isinstance(data, dict) else None
    if not isinstance(info, dict) or not isinstance(messages, list):
        raise ValueError('OpenCode source must be a session export with info and messages')
    if info.get('id') != args.subject_id:
        raise ValueError('Source session metadata does not match subject ID')
    boundary = args.before_message_id or args.through_message_id
    ids = [m.get('id') for m in messages]
    limit = args.cutoff_ms
    # An export omits a message that is still in progress. A fork taken through such a
    # message is then bounded by the fork time alone; nothing else may relax a boundary.
    in_export = ids.count(boundary) == 1
    if in_export:
        end = ids.index(boundary) + (1 if args.through_message_id else 0)
    elif boundary in ids or not args.through_message_id or limit is None:
        raise ValueError('Message boundary did not resolve to exactly one source message')
    else:
        end = len(messages)

    def later(moment):
        return limit is not None and isinstance(moment, (int, float)) and moment > limit

    selected = [m for m in messages[:end] if not later((m.get('time') or {}).get('created'))]
    if not selected:
        raise ValueError('Cutoff did not resolve to a nonempty source prefix')
    child = bool(info.get('parentID'))
    turns, unknown, tools = set(), set(), set()
    runtime, changes, pending = {}, [], []
    latest_usage = None
    total = {'input': 0, 'output': 0, 'reasoning': 0, 'cache_read': 0, 'cache_write': 0}
    requests = 0
    last = None
    for message in selected:
        mid, kind, time = message.get('id'), message.get('type'), message.get('time') or {}
        last = max(v for v in [last, time.get('created')] if v is not None) if time.get('created') else last
        if kind == 'user':
            # A child session's prompts come from its parent agent or a person; records do not say which.
            (unknown if child else turns).add(mid)
        if kind != 'assistant':
            continue
        model = message.get('model') or {}
        name = '/'.join(v for v in (model.get('providerID'), model.get('id')) if v) or None
        for key, value in (('model', name), ('effort', model.get('variant'))):
            if value is not None:
                runtime[key] = {'value': value, 'source_message': mid,
                                'method': 'recorded' if key == 'model' else 'recorded model variant'}
        setting = [runtime.get(k, {}).get('value') for k in ('model', 'effort')]
        if not changes or changes[-1]['settings'] != setting:
            changes.append({'source_message': mid, 'settings': setting})
        for part in message.get('content') or []:
            if not isinstance(part, dict) or part.get('type') != 'tool' or not part.get('id'):
                continue
            part_time = part.get('time') or {}
            if later(part_time.get('created')):
                continue
            tools.add((mid, part['id']))
            done = part_time.get('completed')
            if done is None or later(done):
                pending.append({'source_message': mid, 'tool_id': part['id']})
        usage = message.get('tokens')
        done = time.get('completed')
        if isinstance(usage, dict) and done is not None and not later(done):
            cache = usage.get('cache') or {}
            row = {'input': usage.get('input', 0), 'output': usage.get('output', 0),
                   'reasoning': usage.get('reasoning', 0), 'cache_read': cache.get('read', 0),
                   'cache_write': cache.get('write', 0)}
            for key in total:
                total[key] += row[key]
            requests += 1
            latest_usage = dict(row, source_message=mid)
            runtime['context_used'] = {
                'value': row['input'] + row['cache_read'] + row['cache_write'], 'source_message': mid,
                'method': 'latest completed response input + cache-read + cache-write tokens; not instantaneous'}
            last = max(last or done, done)
    missing = {'value': None, 'status': 'unavailable', 'reason': 'not exposed in native session records'}
    for field in ('harness_version', 'model', 'effort', 'context_used', 'context_capacity'):
        runtime.setdefault(field, dict(missing))
    created = (info.get('time') or {}).get('created')
    as_of = limit if limit is not None else last
    cutoff = {k: getattr(args, k) for k in ('before_message_id', 'through_message_id', 'cutoff_ms')
              if getattr(args, k) is not None}
    cutoff['boundary_in_export'] = in_export
    size = len(json.dumps(selected, ensure_ascii=False, separators=(',', ':')).encode())
    return {'schema': 'agent-issue-metrics/v1', 'harness': 'opencode',
            'subject_id': args.subject_id, 'source': str(Path(args.transcript).resolve()),
            'cutoff': cutoff, 'as_of': iso_ms(as_of) if as_of is not None else None,
            'subject_project_cwd': (info.get('location') or {}).get('directory'),
            'subject_title': info.get('title'), 'subject_parent_id': info.get('parentID'),
            'subject_fork': info.get('fork'),
            'runtime': runtime, 'runtime_changes': changes,
            'session': {'start': iso_ms(created) if created is not None else None,
                        'age_seconds': (as_of - created) / 1000 if None not in (as_of, created) else None,
                        'age_is_lower_bound': created is None,
                        'transcript_kb': None, 'physical_prefix_bytes': None,
                        'export_prefix_bytes': size,
                        'source_records_in_prefix': len(selected), 'human_turns': len(turns),
                        'peer_requests': 0, 'unknown_origin_messages': len(unknown),
                        'tool_invocations': len(tools)},
            'pending_at_cutoff': pending,
            'accounting': {'boundary': 'boundary_in_export false means the through-message was still in progress and absent from the export: the prefix is bounded by cutoff_ms only and that message, including any tool call it had started, is not measured',
                           'turns': 'user-type messages in a top-level session; synthetic, skill, shell, system, and compaction messages excluded; prompts submitted by another program are not distinguishable from typed input',
                           'unknown': 'user-type messages in a session with a parent: the sender is not recorded',
                           'tools': 'unique tool parts started by the cutoff; pending_at_cutoff lists calls whose outcome was not yet recorded, so any outcome shown now is post-cutoff',
                           'size': 'physical transcript size is not exposed; export_prefix_bytes is the compact serialized size of the selected export messages, not a transcript or context measure',
                           'usage': 'responses completed by the cutoff only; session-level totals are not used because they include later and auxiliary generation'},
            'latest_reported_usage': latest_usage,
            'cumulative_usage': dict(total, completed_responses=requests,
                                     method='sum of per-response reported usage in the prefix; not context occupancy')}


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
    m.add_argument('--harness', choices=('codex', 'claude', 'opencode'), required=True)
    m.add_argument('--transcript', required=True)
    m.add_argument('--subject-id', required=True)
    cut = m.add_mutually_exclusive_group(required=True)
    for flag in ('end-ordinal-exclusive', 'end-byte-exclusive', 'end-line-inclusive'):
        cut.add_argument('--'+flag, type=int)
    cut.add_argument('--through-uuid')
    cut.add_argument('--before')
    cut.add_argument('--before-message-id', help='OpenCode: stop before this message')
    cut.add_argument('--through-message-id', help='OpenCode: stop after this message')
    m.add_argument('--cutoff-ms', type=int,
                   help='OpenCode: epoch milliseconds; exclude anything recorded later')
    s = sub.add_parser('save', help='Save reviewed Markdown from stdin, without overwrite')
    s.add_argument('--project', default='unknown-project')
    s.add_argument('--session', default='untitled-session')
    s.add_argument('--captured-at', required=True)
    s.add_argument('--outside', action='append', default=[])
    s.add_argument('--output')
    args = parser.parse_args()
    try:
        if args.command == 'save':
            result = save(args)
        else:
            native = bool(args.before_message_id or args.through_message_id)
            if native != (args.harness == 'opencode') or (args.cutoff_ms is not None and not native):
                raise ValueError('OpenCode needs a message-ID cutoff; other harnesses do not accept one')
            result = opencode_metrics(args) if native else metrics(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc),
                          'intended_output': getattr(args, 'output', None)}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
