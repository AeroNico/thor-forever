"""Read-only archive safety audit before approving a pinned payload hash."""
import posixpath
import sys
import tarfile


def audit(members):
    seen = set()
    links = set()
    paths = []
    total = 0
    for member in members:
        name = member.name
        normalized = posixpath.normpath(name)
        if ('\\' in name or name.startswith('/') or '..' in name.split('/')
                or ':' in name or normalized in ('', '..')):
            raise ValueError('Unsafe member path')
        if normalized == '.' and member.isdir():
            continue
        if normalized in seen:
            raise ValueError('Duplicate member')
        seen.add(normalized)
        paths.append(normalized)
        if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
            raise ValueError('Special file not allowed')
        if member.mode & 0o6000:
            raise ValueError('Privileged permission bits')
        if member.issym() or member.islnk():
            target = member.linkname
            if not target or target.startswith('/') or '\\' in target or ':' in target:
                raise ValueError('Unsafe link target')
            base = posixpath.dirname(normalized) if member.issym() else ''
            resolved = posixpath.normpath(posixpath.join(base, target))
            if resolved == '..' or resolved.startswith('../'):
                raise ValueError('Link escapes extraction root')
            links.add(normalized)
        total += member.size
        if total > 2 * 1024**3 or len(paths) > 20000:
            raise ValueError('Archive size/member limit exceeded')
    for name in paths:
        parent = posixpath.dirname(name)
        while parent:
            if parent in links:
                raise ValueError('Member nested beneath a link')
            parent = posixpath.dirname(parent)
    return len(paths), total


if __name__ == '__main__':
    with tarfile.open(sys.argv[1], 'r:*') as archive:
        count, size = audit(archive)
    print(f'PASS: {count} members; {size} unpacked bytes. No extraction performed.')
