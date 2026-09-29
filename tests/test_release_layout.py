"""Static integration guards for the final package, not a device acceptance test."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseLayoutTests(unittest.TestCase):
    def test_destination_alignment(self):
        for name in ('install-components.sh', 'setup.sh', 'launch-game.sh'):
            with self.subTest(name=name):
                source = (ROOT / 'installer' / name).read_text()
                self.assertIn('/release-v1"', source)
                self.assertNotIn('/install-v1"', source)

    def test_no_private_test_entry_paths(self):
        for name in ('src/launcher.c', 'installer/setup.sh', 'installer/entry.sh',
                     'installer/launch-game.sh', 'Install-Thor-Forever.cmd'):
            with self.subTest(name=name):
                source = (ROOT / name).read_text()
                self.assertNotIn('Thor-Forever-Test-', source)
                self.assertNotIn('install-v2', source)
                self.assertIn('Thor-Forever', source)

    def test_settings_name_matches(self):
        for name in ('installer/stage-game.sh', 'installer/launch-game.sh'):
            self.assertIn('Config-Thor-Forever.wtf', (ROOT / name).read_text())
        self.assertNotIn('-config WTF', (ROOT / 'installer/launch-game.sh').read_text())

    def test_bridge_targets_exist(self):
        self.assertIn('installer/entry.sh', (ROOT / 'src/launcher.c').read_text())
        self.assertIn('installer/launch-game.sh', (ROOT / 'installer/entry.sh').read_text())
        self.assertTrue((ROOT / 'installer/launch-game.sh').is_file())


if __name__ == '__main__':
    unittest.main()
