"""Temporary fixtures only. Pass a Windows busybox.exe path as the argument."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SHELL = str(Path(sys.argv.pop(1)).resolve())
SOURCE = (Path(__file__).parents[1] / 'installer/stage-game.sh').read_text()


class StagingTests(unittest.TestCase):
    def run_case(self, mode):
        with tempfile.TemporaryDirectory(prefix='thor-stage-') as directory:
            root = Path(directory)
            game = root / 'original/World of Warcraft/_classic_beta_'
            game.mkdir(parents=True)
            (game / 'WowB-ARM64.exe').write_bytes(b'fixture-executable')
            (game / 'WTF').mkdir()
            (game / 'WTF/Account.txt').write_text('private-fixture')
            (game / 'WTF/Config.wtf').write_text('original-settings')
            install = root / 'dedicated'
            install.mkdir()
            (install / 'components-ready').write_text('COMPONENTS_READY')
            (root / 'starter.wtf').write_text('starter-settings')
            if mode != 'missing-data':
                data = game / 'Data' if mode == 'child-data' else game.parent / 'Data'
                data.mkdir()
                (data / 'fixture').write_text('shared-data')
            if mode == 'existing':
                (install / 'game').mkdir()
                (install / 'game/keep').write_text('do-not-touch')
            # Host portability shim only; Android uses mksh's print builtin.
            script = 'print() { shift; shift; printf "%s\\n" "$*"; }\n' + SOURCE
            script += '\ntf_stage_game "$1" "$2" "$3"\n'
            result = subprocess.run(
                [SHELL, 'sh', '-c', script, 'test', game.as_posix(),
                 install.as_posix(), (root / 'starter.wtf').as_posix()],
                capture_output=True, text=True)
            if mode in ('missing-data', 'existing'):
                self.assertEqual(result.returncode, 55 if mode == 'missing-data' else 54, result.stderr)
                self.assertFalse((install / 'game-ready').exists())
                if mode == 'existing':
                    self.assertEqual((install / 'game/keep').read_text(), 'do-not-touch')
            else:
                if result.returncode == 60 and sys.platform == 'win32' and 'Permission denied' in result.stderr:
                    self.assertFalse((install / 'game-ready').exists())
                    self.assertEqual((game / 'WTF/Config.wtf').read_text(), 'original-settings')
                    self.skipTest('Windows denied directory symlink creation; Android validation required')
                self.assertEqual(result.returncode, 0, result.stderr)
                staged = install / 'game/_classic_beta_'
                self.assertEqual((staged / 'WowB-ARM64.exe').read_bytes(), b'fixture-executable')
                self.assertFalse((staged / 'WTF/Account.txt').exists())
                self.assertEqual((staged / 'WTF/Config-Thor-Forever.wtf').read_text(), 'starter-settings')
                link = staged / 'Data' if mode == 'child-data' else install / 'game/Data'
                self.assertTrue(link.is_symlink())
                self.assertEqual((link / 'fixture').read_text(), 'shared-data')
            self.assertEqual((game / 'WTF/Config.wtf').read_text(), 'original-settings')

    def test_parent_data(self): self.run_case('parent-data')
    def test_child_data(self): self.run_case('child-data')
    def test_existing_refused(self): self.run_case('existing')
    def test_missing_data(self): self.run_case('missing-data')


if __name__ == '__main__':
    unittest.main()
