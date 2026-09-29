"""Remove only unused upstream prefix-import files from the tested runtime.

Never modifies the input archive or an installed runtime. The retained member
contents and metadata are verified against the pinned input after packaging.
"""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tarfile

INPUT_SHA256 = '41d22dca5c6ede633e59971f16bf180e449583648b4c804027e23353cce1a453'
EXCLUDED = frozenset({'prefixPack.txz', 'profile.json'})


def digest(path):
    with open(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def identity(archive, member):
    content = None
    if member.isfile():
        with archive.extractfile(member) as stream:
            content = hashlib.file_digest(stream, 'sha256').hexdigest()
    return (member.type, member.mode, member.uid, member.gid, member.mtime,
            member.size, member.linkname, member.uname, member.gname, content)


def prepare(source, destination):
    if digest(source) != INPUT_SHA256:
        raise ValueError('Input is not the pinned, tested upstream runtime')
    spec = importlib.util.spec_from_file_location('archive_audit', Path(__file__).with_name('audit-runtime-archive.py'))
    audit_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_module)
    with tarfile.open(source, 'r:') as original:
        members = original.getmembers()
        audit_module.audit(members)
        if not EXCLUDED.issubset({m.name for m in members}):
            raise ValueError('Expected upstream import metadata is missing')
        expected = {m.name: identity(original, m) for m in members if m.name not in EXCLUDED}
        # Exclusive creation: no existing output is overwritten.
        with open(destination, 'xb') as stream:
            with tarfile.open(fileobj=stream, mode='w', format=tarfile.PAX_FORMAT) as output:
                for member in members:
                    if member.name in EXCLUDED:
                        continue
                    if member.isfile():
                        with original.extractfile(member) as content:
                            output.addfile(member, content)
                    else:
                        output.addfile(member)
    with tarfile.open(destination, 'r:') as output:
        audit_module.audit(output.getmembers())
        actual = {m.name: identity(output, m) for m in output}
    if actual != expected:
        raise ValueError('Output verification failed; do not distribute output')
    print(f'PASS: {len(actual)} retained members identical; excluded only {sorted(EXCLUDED)}')
    print(f'{digest(destination)}  {Path(destination).name}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: prepare-runtime.py INPUT.tar NEW-OUTPUT.tar')
    prepare(Path(sys.argv[1]), Path(sys.argv[2]))
