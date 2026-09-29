"""Verify a staged candidate and produce a new release ZIP. Never uploads."""
import hashlib
from pathlib import Path
import re
import sys
import zipfile

LAUNCHER = '311918c59c089352853035caa8abf5984fe37c41378bc2472aff1407161ccd79'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def finalize(kit, output):
    manifest = kit / 'CANDIDATE-SHA256.txt'
    expected = {}
    for line in manifest.read_text(encoding='utf-8-sig').splitlines()[1:]:
        match = re.fullmatch(r'([a-f0-9]{64})  (.+)', line)
        if not match or match[2] in expected:
            raise ValueError('Invalid candidate manifest')
        expected[match[2]] = match[1]
    actual = {}
    for path in kit.rglob('*'):
        if path.is_symlink():
            raise ValueError('No symlinks in the staged release kit')
        if path.is_file() and path != manifest:
            actual[path.relative_to(kit).as_posix()] = sha(path)
    if actual != expected:
        raise ValueError('Staged files differ from the candidate manifest')
    if actual.get('Thor-Forever.exe') != LAUNCHER:
        raise ValueError('Not the device-tested launcher')
    root = Path(__file__).resolve().parents[1]
    pins = re.findall(r'^([a-f0-9]{64}) ([^\s]+)$', (root / 'installer/verify-payload.sh').read_text(), re.M)
    if len(pins) != 7 or any(actual.get('payload/' + name) != digest for digest, name in pins):
        raise ValueError('Pinned payload mismatch')
    sums = ''.join(f'{digest}  {name}\n' for name, digest in sorted(actual.items()))
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
        for name in sorted(actual):
            archive.write(kit / name, 'Thor-Forever/' + name)
        archive.writestr('Thor-Forever/SHA256SUMS.txt', sums)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('Release ZIP integrity failure')
    print(f'PASS: {len(actual)} files verified; ZIP integrity passed')
    print(sha(output), output.name)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: finalize-kit.py STAGED-Thor-Forever NEW-OUTPUT.zip')
    finalize(Path(sys.argv[1]), Path(sys.argv[2]))
