import importlib.util
from pathlib import Path
import tarfile
import unittest

spec = importlib.util.spec_from_file_location('audit_runtime', Path(__file__).parents[1] / 'tools/audit-runtime-archive.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def member(name, kind=tarfile.REGTYPE, target=''):
    item = tarfile.TarInfo(name)
    item.type = kind
    item.linkname = target
    return item


class ArchiveAuditTests(unittest.TestCase):
    def test_safe_runtime_link(self):
        self.assertEqual(module.audit([member('bin/wine', tarfile.SYMTYPE, '../lib/wine'), member('lib/wine')])[0], 2)

    def test_unsafe(self):
        cases = [
            [member('/absolute')], [member('../escape')],
            [member('x', tarfile.SYMTYPE, '../../escape')],
            [member('x', tarfile.SYMTYPE, '/system')],
            [member('x', tarfile.CHRTYPE)],
            [member('x'), member('x')],
            [member('bin', tarfile.SYMTYPE, 'elsewhere'), member('bin/wine')],
            [member('x', tarfile.LNKTYPE, '../escape')],
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                module.audit(case)


if __name__ == '__main__':
    unittest.main()
