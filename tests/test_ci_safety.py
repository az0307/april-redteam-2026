import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class SafetyChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)

    def track(self, name, content='placeholder'):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        subprocess.run(['git', '-C', str(self.repo), 'add', '-f', name], check=True)

    def scan(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        commands = '\n'.join(step['run'] for step in workflow['jobs']['secret-scan']['steps']
                             if 'run' in step)
        if (ROOT / 'ci').exists():
            shutil.copytree(ROOT / 'ci', self.repo / 'ci', dirs_exist_ok=True)
        return subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', commands],
                              cwd=self.repo, capture_output=True, text=True)

    def test_templates_and_whitespace_paths_are_scanned_without_disclosing_values(self):
        for name in ['.env.example', '.github/workflows/ci.yml', 'space name.txt']:
            with self.subTest(name=name):
                token = 'ghp_' + 'a' * 36  # Synthetic fixture, never a real credential.
                self.track(name, token)
                result = self.scan()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(name, result.stdout)
                self.assertNotIn(token, result.stdout + result.stderr)

    def test_scan_fails_closed_when_tracked_file_cannot_be_read(self):
        self.track('missing.txt')
        (self.repo / 'missing.txt').unlink()
        self.assertNotEqual(self.scan().returncode, 0)

    def test_only_exact_loot_scaffold_is_allowed(self):
        for name in ['loot/README.md', 'loot/REPORT_TEMPLATE.md',
                     'loot/mission-template/mission.md', 'loot/mission-template/findings.md']:
            self.track(name)
        self.assertEqual(self.scan().returncode, 0)
        self.track('loot/customer/README_credentials.txt')
        self.assertNotEqual(self.scan().returncode, 0)

    def test_environment_backup_is_rejected(self):
        self.track('.env.bak.20260101')
        self.assertNotEqual(self.scan().returncode, 0)

    def test_safe_placeholder_template_passes(self):
        self.track('.env.example', 'API_KEY=your-key-here\n')
        self.assertEqual(self.scan().returncode, 0)

    def test_each_existing_key_shape_is_detected(self):
        fixtures = ['sk-ant-api03-' + 'a' * 24, 'sk-proj-' + 'b' * 24,
                    'AKIA' + 'A' * 16, 'ghp_' + 'c' * 36, 'sk-' + 'd' * 48]
        for token in fixtures:
            self.track('fixture.txt', token)
            result = self.scan()
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(token, result.stdout + result.stderr)

    def test_makefile_validation_propagates_parse_failure(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        step = workflow['jobs']['validate-makefile']['steps'][-1]
        (self.repo / 'Makefile').write_text('not valid make syntax\n')
        result = subprocess.run(['bash', '-e', '-c', step['run']],
                                cwd=self.repo, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_summary_rejects_failed_cancelled_and_skipped_dependencies(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        job = workflow['jobs']['ci-summary']
        step = job['steps'][0]
        self.assertIn('NEEDS_JSON', step.get('env', {}))
        for status in ['failure', 'cancelled', 'skipped', 'success']:
            needs = {name: {'result': 'success'} for name in job['needs']}
            needs[job['needs'][0]]['result'] = status
            result = subprocess.run(['bash', '-e', '-c', step['run']],
                                    env={**os.environ, 'NEEDS_JSON': json.dumps(needs)},
                                    capture_output=True)
            self.assertEqual(result.returncode == 0, status == 'success', status)

    def test_mission_name_cannot_escape_loot_or_break_template_substitution(self):
        (self.repo / 'scripts').mkdir()
        shutil.copy(ROOT / 'scripts/new-mission.sh', self.repo / 'scripts/new-mission.sh')
        for name in ['../outside', 'bad/name', 'bad&name', '..', '-option']:
            with self.subTest(name=name):
                result = subprocess.run(['bash', str(self.repo / 'scripts/new-mission.sh'),
                                         name, 'example.invalid', 'web'], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.repo / 'outside').exists())
        result = subprocess.run(['bash', str(self.repo / 'scripts/new-mission.sh'),
                                 'safe-mission_01', 'example.invalid', 'web'], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual((self.repo / 'loot/safe-mission_01/scope.txt').read_text(),
                         'example.invalid\n')


if __name__ == '__main__':
    unittest.main()
