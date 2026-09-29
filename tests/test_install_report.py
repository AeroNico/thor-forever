"""Exercise success and each failure-phase report without Android or real payloads."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SHELL = str(Path(sys.argv.pop(1)).resolve())
SOURCE = (Path(__file__).parents[1] / 'installer/install-report.sh').read_text()


class ReportTests(unittest.TestCase):
    def test_reports(self):
        for phase in ('payload', 'storage', 'extraction', 'components', 'prefix', 'dxvk', 'game', 'unknown', 'prepared'):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(prefix='thor-report-') as directory:
                code = '0' if phase == 'prepared' else '21'
                script = 'print() { shift; shift; printf "%s\\n" "$*"; }\n' + SOURCE
                script += '\nTF_INSTALL=$1; TF_PHASE=$2; tf_install_report "$3"\n'
                subprocess.run([SHELL, 'sh', '-c', script, 'test', Path(directory).as_posix(), phase, code], check=True)
                report = (Path(directory) / 'result.txt').read_text()
                self.assertIn('PHASE=' + phase, report)
                self.assertIn('EXIT_CODE=' + code, report)
                self.assertIn('STATUS=' + ('PREPARED_NOT_VALIDATED' if code == '0' else 'STOPPED'), report)
                self.assertNotIn(directory, report)


if __name__ == '__main__':
    unittest.main()
