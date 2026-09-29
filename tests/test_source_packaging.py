"""Temporary fixtures only; no downloaded code is executed."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('sources', Path(__file__).parents[1] / 'tools/package-sources.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourcePackagingTests(unittest.TestCase):
    def fixture(self, path, count=16, unexpected=False):
        with tarfile.open(path, 'w:gz') as archive:
            files = {'wine/src/example.c': b'/* retained source */\n'}
            files.update({f'wine/android/wayland-deps/usr/lib/lib{x}.so': b'\x7fELFfixture' for x in range(count)})
            if unexpected:
                files['wine/unexpected.exe'] = b'MZfixture'
            for name, data in files.items():
                member = tarfile.TarInfo(name)
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))

    def test_preserves_source_and_records_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.tar.gz'
            self.fixture(path)
            data, omitted = module.filtered_wine(path)
            self.assertEqual(len(omitted), 16)
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                self.assertEqual(archive.getnames(), ['wine/src/example.c'])
                self.assertEqual(archive.extractfile('wine/src/example.c').read(), b'/* retained source */\n')

    def test_refuses_changed_vendor_count(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.tar.gz'
            self.fixture(path, count=15)
            with self.assertRaises(ValueError):
                module.filtered_wine(path)

    def test_refuses_unexpected_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.tar.gz'
            self.fixture(path, unexpected=True)
            with self.assertRaises(ValueError):
                module.filtered_wine(path)


if __name__ == '__main__':
    unittest.main()
