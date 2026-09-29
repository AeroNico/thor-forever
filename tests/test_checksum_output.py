"""Check exact digest/path matching despite observed GameHub wrapper messages."""
from pathlib import Path
import subprocess
import sys
import unittest

SHELL = str(Path(sys.argv.pop(1)).resolve())
SOURCE = (Path(__file__).parents[1] / 'installer/verify-payload.sh').read_text()
DIGEST = '41d22dca5c6ede633e59971f16bf180e449583648b4c804027e23353cce1a453'
EXPECTED = DIGEST + '  /fixture path/wine-runtime.tar'
NOISE = ('Could not find memory region containing address /wine'
         'Could not find memory region containing address /box64')


class ChecksumTests(unittest.TestCase):
    def test_exact_matching(self):
        cases = [
            (EXPECTED, True),
            (NOISE + EXPECTED, True),
            ('Failed to inject process' + NOISE + EXPECTED, True),
            (NOISE, False),
            (NOISE + EXPECTED.replace(DIGEST, '0' * 64), False),
            (NOISE + EXPECTED + '.other', False),
            ('unknown-prefix' + EXPECTED, False),
            (EXPECTED + ' unexpected-suffix', False),
            (DIGEST, False),
            (NOISE + EXPECTED.replace('  /', ' /'), False),
        ]
        for line, accepted in cases:
            with self.subTest(line=line):
                result = subprocess.run(
                    [SHELL, 'sh', '-c', SOURCE + '\ntf_checksum_line_matches "$1" "$2"',
                     'test', line, EXPECTED], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if accepted else 1, result.stderr)


if __name__ == '__main__':
    unittest.main()
