"""Focused checks for source accounting and non-destructive private packet output."""
import argparse
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'plugins/agentic-devcraft/skills/capture-agent-issue/scripts/capture_support.py'
spec = importlib.util.spec_from_file_location('capture_support', SOURCE)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


class CaptureSupportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def source(self, rows):
        p = self.root / 'source.jsonl'
        p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        return p

    def measure(self, harness, rows, **cutoff):
        args = dict(harness=harness, subject_id='subject', transcript=str(self.source(rows)),
                    end_ordinal_exclusive=None, end_byte_exclusive=None,
                    end_line_inclusive=None, through_uuid=None, before=None)
        args.update(cutoff)
        return support.metrics(argparse.Namespace(**args))

    def test_codex_paginated_provenance_and_cutoff_exclude_generated_and_later_activity(self):
        rows = [
            {'ordinal': 0, 'timestamp': '2026-11-06T10:00:00Z', 'type': 'session_meta',
             'payload': {'id': 'subject', 'timestamp': '2026-11-06T10:00:00Z', 'cli_version': 'test'}},
            {'ordinal': 1, 'type': 'turn_context', 'payload': {'model': 'test-model', 'effort': 'high'}},
            {'ordinal': 2, 'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'id': 'human',
              'content': [{'text': 'PRIVATE text must not be emitted'}],
              'internal_chat_message_metadata_passthrough': {'content_item_kinds': ['user.text']}}},
            {'ordinal': 3, 'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'id': 'generated',
              'internal_chat_message_metadata_passthrough': {'content_item_kinds': ['skills.selected_skill_instructions']}}},
            {'ordinal': 4, 'type': 'response_item', 'origin': {'kind': 'peer'},
             'payload': {'type': 'message', 'role': 'user', 'id': 'peer'}},
            {'ordinal': 5, 'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'call-1'}},
            {'ordinal': 6, 'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'call-1'}},
            {'ordinal': 7, 'timestamp': '2026-11-06T10:01:00Z', 'type': 'event_msg', 'payload': {
             'type': 'token_count', 'info': {'last_token_usage': {'total_tokens': 123},
             'total_token_usage': {'total_tokens': 99999}, 'model_context_window': 1000}}},
            {'ordinal': 8, 'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'capture-call'}},
        ]
        result = self.measure('codex', rows, end_ordinal_exclusive=8)
        self.assertEqual(result['session']['human_turns'], 1)
        self.assertEqual(result['session']['peer_requests'], 1)
        self.assertEqual(result['session']['tool_invocations'], 1)
        self.assertEqual(result['runtime']['context_used']['value'], 123)
        self.assertEqual(result['session']['age_seconds'], 60)
        self.assertEqual(result['session']['physical_prefix_bytes'],
                         len(''.join(json.dumps(r)+'\n' for r in rows[:8]).encode()))
        self.assertNotIn('PRIVATE', json.dumps(result))

    def test_codex_legacy_user_event_does_not_double_count_response_copy(self):
        rows = [{'ordinal': 0, 'type': 'session_meta', 'payload': {'id': 'subject'}},
                {'ordinal': 1, 'type': 'event_msg', 'payload': {'type': 'user_message', 'id': 'human'}},
                {'ordinal': 2, 'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'id': 'copy',
                  'internal_chat_message_metadata_passthrough': {'content_item_kinds': ['user.text']}}}]
        self.assertEqual(self.measure('codex', rows, end_ordinal_exclusive=3)['session']['human_turns'], 1)

    def test_claude_authorship_repeated_calls_and_source_cutoff(self):
        def event(kind, uid, **fields):
            return {'type': kind, 'uuid': uid, 'sessionId': 'subject',
                    'timestamp': '2026-11-06T10:00:00Z', **fields}
        rows = [event('user', 'h', origin={'kind': 'human'}, message={'content': 'issue'}),
                event('user', 'peer', origin={'kind': 'peer'}, isMeta=True),
                event('user', 'meta', origin={'kind': 'human'}, isMeta=True),
                event('user', 'compact', isCompactSummary=True),
                event('user', 'result', message={'content': [{'type': 'tool_result', 'tool_use_id': 'old'}]}),
                event('user', 'unknown', message={'content': 'unknown origin'}),
                event('assistant', 'a1', version='test', effort='high', message={'id': 'response', 'model': 'test',
                  'content': [{'type': 'tool_use', 'id': 'pending'}],
                  'usage': {'input_tokens': 3, 'cache_creation_input_tokens': 5, 'cache_read_input_tokens': 7}}),
                event('assistant', 'cutoff', message={'id': 'response',
                  'content': [{'type': 'tool_use', 'id': 'pending'}],
                  'usage': {'input_tokens': 3, 'cache_creation_input_tokens': 5, 'cache_read_input_tokens': 7}}),
                event('user', 'synthetic', sessionId='collector', message={'content': [
                  {'type': 'tool_result', 'tool_use_id': 'pending', 'is_error': True}]}),
                event('user', 'later-success', message={'content': [
                  {'type': 'tool_result', 'tool_use_id': 'pending', 'is_error': False}]}),
                event('assistant', 'later-tool', message={'content': [{'type': 'tool_use', 'id': 'later'}]})]
        result = self.measure('claude', rows, through_uuid='cutoff')
        self.assertEqual(result['session']['human_turns'], 1)
        self.assertEqual(result['session']['peer_requests'], 1)
        self.assertEqual(result['session']['unknown_origin_messages'], 1)
        self.assertEqual(result['session']['tool_invocations'], 1)
        self.assertEqual(result['runtime']['context_used']['value'], 15)
        self.assertIsNone(result['runtime']['context_capacity']['value'])
        self.assertTrue(result['session']['age_is_lower_bound'])

    def test_invalid_boundary_or_subject_cannot_silently_select_entire_file(self):
        rows = [{'ordinal': 0, 'type': 'session_meta', 'payload': {'id': 'other'}}]
        with self.assertRaisesRegex(ValueError, 'subject ID'):
            self.measure('codex', rows, end_ordinal_exclusive=1)
        with self.assertRaisesRegex(ValueError, 'Cutoff'):
            self.measure('claude', rows, through_uuid='missing')
        with self.assertRaisesRegex(ValueError, 'boundary'):
            self.measure('claude', rows, end_byte_exclusive=3)

    def save(self, body='# Synthetic packet\n', **fields):
        args = dict(project='Project É $(literal)', session='Original Session',
                    captured_at='2026-11-06T12:34:00-05:00', output=None, outside=[str(ROOT)])
        args.update(fields)
        data = io.TextIOWrapper(io.BytesIO(body.encode()), encoding='utf-8')
        with patch.object(support.tempfile, 'gettempdir', return_value=str(self.root)), patch.object(support.sys, 'stdin', data):
            return support.save(argparse.Namespace(**args))

    def test_save_preserves_names_utc_frozen_minute_unique_paths_and_private_payload(self):
        first = self.save();second = self.save()
        p = Path(first['path'])
        self.assertNotEqual(first['path'], second['path'])
        self.assertEqual(p.parent.parent.name, 'Original Session')
        self.assertEqual(p.parent.parent.parent.name, 'Project É $(literal)')
        self.assertTrue(p.parent.name.startswith('2026-11-06T17-34Z-'))
        self.assertEqual(p.read_text(), '# Synthetic packet\n')
        self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(p.parent.stat().st_mode), 0o700)
        self.assertEqual(first['sha256'], support.hashlib.sha256(p.read_bytes()).hexdigest())

    def test_explicit_destination_is_exclusive_and_has_no_fallback(self):
        p = self.root/'chosen.md';p.write_text('existing')
        with self.assertRaises(FileExistsError):
            self.save(output=str(p))
        self.assertEqual(p.read_text(), 'existing')
        self.assertFalse((self.root/'agent-issues').exists())
        with patch.object(support.os, 'open', side_effect=PermissionError('synthetic denied destination')):
            with self.assertRaises(PermissionError):
                self.save(output=str(self.root/'denied.md'))
        self.assertFalse((self.root/'agent-issues').exists())

    def test_default_rejects_worktree_temp_and_contained_output_directory(self):
        with self.assertRaisesRegex(ValueError, 'worktree'):
            self.save(outside=[str(self.root)])
        with self.assertRaisesRegex(ValueError, 'worktree'):
            self.save(outside=[str(self.root/'agent-issues')])
        self.assertFalse((self.root/'agent-issues').exists())

    def test_missing_names_use_explicit_fallbacks_without_replacing_known_names(self):
        p = Path(self.save(project='', session='')['path'])
        self.assertEqual(p.parent.parent.name, 'untitled-session')
        self.assertEqual(p.parent.parent.parent.name, 'unknown-project')

    def test_path_representation_only_changes_required_characters_and_rejects_symlinks(self):
        result = self.save(project='Named/Project', session='..')
        p = Path(result['path'])
        self.assertEqual(p.parent.parent.name, 'untitled-session')
        self.assertEqual(p.parent.parent.parent.name, 'Named - Project')
        # A planted output base must not redirect the default outside its temp subtree.
        other = self.root/'other';other.mkdir()
        base = self.root/'agent-issues'
        # Use a separate temp root, without touching the successful packet.
        alternative = self.root/'alternative';alternative.mkdir()
        (alternative/'agent-issues').symlink_to(other, target_is_directory=True)
        with patch.object(support.tempfile, 'gettempdir', return_value=str(alternative)):
            with self.assertRaisesRegex(ValueError, 'symlink'):
                args=argparse.Namespace(project='p',session='s',captured_at='2026-11-06T17:00:00Z',outside=[],output=None)
                with patch.object(support.sys,'stdin',io.TextIOWrapper(io.BytesIO(b'# draft'))):
                    support.save(args)


if __name__ == '__main__':
    unittest.main()
