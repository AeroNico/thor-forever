"""Host tests: pass the path to a POSIX-compatible shell (e.g. busybox sh).
Run: python tests/test_discovery.py /path/to/busybox.exe
Uses temporary fixtures only, never a real GameHub installation.
"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SHELL = sys.argv.pop(1)
SOURCE = (pathlib.Path(__file__).parents[1] / 'installer/discover-game.sh').read_text()


class DiscoveryTests(unittest.TestCase):
    def run_case(self, layouts, expected, empty=False):
        with tempfile.TemporaryDirectory(prefix='thor-forever-test-') as directory:
            root = pathlib.Path(directory)
            for container, programs in layouts:
                game = root / 'usr/home/virtual_containers' / container / 'drive_c' / programs / 'World of Warcraft/_classic_beta_'
                game.mkdir(parents=True)
                (game / 'WowB-ARM64.exe').write_bytes(b'' if empty else b'fixture-not-a-real-game')
            script = SOURCE + '\ntf_discover_game usr\nresult=$?\nprintf "%s:%s:%s\\n" "$result" "$TF_GAME_COUNT" "$TF_DISCOVERY_STATUS"\n'
            result = subprocess.run([SHELL, 'sh'], input=script, text=True, cwd=root, capture_output=True, check=True)
            self.assertEqual(result.stdout.strip(), expected)

    def test_missing(self):
        self.run_case([], '10:0:missing')

    def test_standard_with_spaces(self):
        self.run_case([('local_random', 'Program Files (x86)')], '0:1:found')

    def test_other_program_files(self):
        self.run_case([('local_different', 'Program Files')], '0:1:found')

    def test_multiple(self):
        self.run_case([('one', 'Program Files'), ('two', 'Program Files')], '11:2:multiple')

    def test_empty_executable(self):
        self.run_case([('one', 'Program Files')], '10:0:missing', empty=True)

    def test_shell_metacharacters_are_data(self):
        self.run_case([('local_$(false);with spaces', 'Program Files')], '0:1:found')


if __name__ == '__main__':
    unittest.main()
