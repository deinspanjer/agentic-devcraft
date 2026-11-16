"""Packaging checks for the OpenCode catalog: complete payload, no debris, agreed versions."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'scripts/build_opencode_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)
SHA = 'a' * 40


class CatalogTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.skills = self.root / 'plugin/skills'
        for path, text in {'demo/SKILL.md': '# demo\n', 'demo/references/harness/x.md': 'nested\n',
                           'demo/scripts/__pycache__/x.cpython-312.pyc': 'cache',
                           'demo/.DS_Store': 'debris', 'not-a-skill/notes.md': 'no entrypoint\n'}.items():
            (self.skills / path).parent.mkdir(parents=True, exist_ok=True)
            (self.skills / path).write_text(text)

    def manifests(self, claude, codex):
        for name, version in (('.claude-plugin', claude), ('.codex-plugin', codex)):
            (self.root / 'plugin' / name).mkdir(exist_ok=True)
            (self.root / 'plugin' / name / 'plugin.json').write_text(json.dumps({'version': version}))

    def test_nested_resource_is_published_and_debris_is_not(self):
        out = self.root / 'site'
        index = catalog.build(self.skills, 'plugin/skills', out, '1.2.3', SHA)
        self.assertEqual(index, {'skills': [{'name': 'demo', 'version': '1.2.3', 'files': [
            'SKILL.md', 'references/harness/x.md', 'release.json']}]})
        base = out / 'opencode/skills'
        published = sorted(p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file())
        self.assertEqual(published, ['demo/SKILL.md', 'demo/references/harness/x.md',
                                     'demo/release.json', 'index.json'])
        record = json.loads((base / 'demo/release.json').read_text())
        self.assertEqual((record['skill'], record['version'], record['revision'], record['source_path']),
                         ('demo', '1.2.3', SHA, 'plugin/skills/demo'))

    def test_symlink_in_payload_is_refused(self):
        outside = self.root / 'private.md'
        outside.write_text('private\n')
        os.symlink(outside, self.skills / 'demo/references/leak.md')
        with self.assertRaisesRegex(catalog.CatalogError, 'Symlink'):
            catalog.build(self.skills, 'plugin/skills', self.root / 'site', '1.2.3', SHA)

    def test_disagreeing_release_inputs_are_refused(self):
        self.manifests('1.2.3', '1.2.3')
        self.assertEqual(catalog.release_version(self.root / 'plugin', 'v1.2.3'), '1.2.3')
        for tag in ('v1.2.4', '1.2.3'):
            with self.assertRaisesRegex(catalog.CatalogError, 'disagree'):
                catalog.release_version(self.root / 'plugin', tag)
        self.manifests('1.2.3', '1.2.2')
        with self.assertRaisesRegex(catalog.CatalogError, 'disagree'):
            catalog.release_version(self.root / 'plugin', 'v1.2.3')


if __name__ == '__main__':
    unittest.main()
