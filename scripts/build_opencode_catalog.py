#!/usr/bin/env python3
"""Build the OpenCode HTTP skill catalog from the released skill payload. Stdlib only.

Writes <output>/opencode/skills/index.json plus one complete directory per skill,
each with a generated release.json. The output is build output, never a skill source.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
PLUGIN = 'plugins/agentic-devcraft'
REPOSITORY = 'https://github.com/deinspanjer/agentic-devcraft'
SCHEMA = 'agentic-devcraft-skill-release/v1'
RELEASE_FILE = 'release.json'
SKIP_DIRS = {'__pycache__', 'node_modules'}
SKIP_SUFFIXES = {'.pyc', '.pyo', '.swp', '.orig', '.rej'}


class CatalogError(Exception):
    pass


def release_version(plugin_root, tag):
    """Return the one version shared by the release tag and both package manifests."""
    found = {'release tag': tag[1:] if tag.startswith('v') else None}
    for name in ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
        try:
            found[name] = json.loads((plugin_root / name).read_text(encoding='utf-8')).get('version')
        except (OSError, ValueError) as error:
            raise CatalogError(f'Cannot read {name}: {error}') from error
    if None in found.values() or len(set(found.values())) != 1:
        detail = ', '.join(f'{key}={value!r}' for key, value in found.items())
        raise CatalogError(f'Release versions disagree or are missing (tag {tag!r}): {detail}')
    return found['release tag']


def payload_files(skill_dir):
    """List a skill's regular files as sorted relative POSIX paths; refuse symlinks."""
    files = []
    for path in sorted(skill_dir.rglob('*')):
        relative = path.relative_to(skill_dir)
        if any(part in SKIP_DIRS or part.startswith('.') for part in relative.parts):
            continue
        if path.is_symlink():
            raise CatalogError(f'Symlink in released payload: {path}')
        if path.is_dir() or path.suffix in SKIP_SUFFIXES or path.name.endswith('~'):
            continue
        if not path.is_file():
            raise CatalogError(f'Unsupported file type in released payload: {path}')
        files.append(relative.as_posix())
    if RELEASE_FILE in files:
        raise CatalogError(f'{skill_dir.name}: {RELEASE_FILE} is generated and must not exist in the source')
    return files


def build(skills_root, source_root, output, version, revision):
    """Write the catalog under output/opencode/skills and return the index."""
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise CatalogError('Revision must be a full 40-character commit SHA')
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise CatalogError(f'Released skill root is not a real directory: {skills_root}')
    if output.exists() and any(output.iterdir()):
        raise CatalogError(f'Output directory is not empty: {output}')
    catalog = output / 'opencode' / 'skills'
    entries = []
    for skill_dir in sorted(p for p in skills_root.iterdir() if not p.name.startswith('.')):
        if skill_dir.is_symlink():
            raise CatalogError(f'Symlink in released payload: {skill_dir}')
        if not (skill_dir / 'SKILL.md').is_file():
            continue
        name = skill_dir.name
        files = payload_files(skill_dir)
        for relative in files:
            target = catalog / name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(skill_dir / relative, target)
        record = {'schema': SCHEMA, 'skill': name, 'version': version, 'repository': REPOSITORY,
                  'source_path': f'{source_root}/{name}', 'revision': revision}
        (catalog / name / RELEASE_FILE).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
        entries.append({'name': name, 'version': version, 'files': sorted(files + [RELEASE_FILE])})
    if not entries:
        raise CatalogError(f'No skills found under {skills_root}')
    index = {'skills': entries}
    (catalog / 'index.json').write_text(json.dumps(index, indent=2) + '\n', encoding='utf-8')
    check(catalog)
    return index


def check(catalog):
    """Fail unless the index and the files on disk describe each other exactly."""
    index = json.loads((catalog / 'index.json').read_text(encoding='utf-8'))
    listed = {'index.json'}
    for entry in index['skills']:
        if 'SKILL.md' not in entry['files']:
            raise CatalogError(f"{entry['name']}: entry has no SKILL.md")
        for relative in entry['files']:
            parts = Path(relative).parts
            if Path(relative).is_absolute() or '..' in parts or '\\' in relative:
                raise CatalogError(f"{entry['name']}: unsafe path {relative!r}")
            listed.add(f"{entry['name']}/{relative}")
    present = {p.relative_to(catalog).as_posix() for p in catalog.rglob('*') if not p.is_dir()}
    if listed != present:
        raise CatalogError(f'Index and output differ: {sorted(listed ^ present)}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--output', required=True, help='Empty or new site directory to write')
    parser.add_argument('--tag', required=True, help='Release tag, v<version>')
    parser.add_argument('--revision', help='Full commit SHA of the release (default: git HEAD)')
    args = parser.parse_args(argv)
    try:
        revision = args.revision or subprocess.run(
            ['git', '-C', str(REPO), 'rev-parse', 'HEAD'], check=True, capture_output=True,
            text=True).stdout.strip()
        version = release_version(REPO / PLUGIN, args.tag)
        index = build(REPO / PLUGIN / 'skills', f'{PLUGIN}/skills', Path(args.output).resolve(),
                      version, revision)
    except (CatalogError, OSError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    for entry in index['skills']:
        print(f"{entry['name']} {entry['version']} {len(entry['files'])} files")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
