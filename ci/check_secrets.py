#!/usr/bin/env python3
"""Check every tracked file; report paths only and fail on unreadable files."""
import os
from pathlib import Path
import re
import subprocess
import sys


KEY_PATTERN = re.compile(
    rb'sk-ant-api[0-9]{2}-[A-Za-z0-9_-]{24}|'
    rb'sk-proj-[A-Za-z0-9_-]{24}|'
    rb'AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{48}'
)
LOOT_SCAFFOLD = {
    'loot/README.md', 'loot/REPORT_TEMPLATE.md',
    'loot/mission-template/mission.md', 'loot/mission-template/findings.md',
}


def main():
    try:
        tracked = subprocess.check_output(['git', 'ls-files', '-z'])
    except subprocess.CalledProcessError:
        print('ERROR: could not enumerate tracked files')
        return 1
    failed = False
    for raw in tracked.split(b'\0'):
        if not raw:
            continue
        name = os.fsdecode(raw)
        path = Path(name)
        if (path.name == '.env' or path.name.startswith('.env.')) and path.name != '.env.example':
            print(f'ERROR: tracked environment file: {name!r}')
            failed = True
        if name.startswith('loot/') and name not in LOOT_SCAFFOLD:
            print(f'ERROR: tracked engagement data: {name!r}')
            failed = True
        try:
            if path.is_symlink():
                raise OSError('tracked symlink cannot be safely scanned')
            data = path.read_bytes()
        except OSError:
            print(f'ERROR: cannot safely read tracked file: {name!r}')
            failed = True
            continue
        if KEY_PATTERN.search(data):
            print(f'ERROR: potential API key in tracked file: {name!r}')
            failed = True
    if not failed:
        print('All tracked files passed secret and evidence checks')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
