#!/usr/bin/python3

from pathlib import Path
import subprocess

folder_path = Path(__file__).resolve().parent
for rule in folder_path.glob("*.rules"):
    cmd = f'sudo ln -sf {rule} /etc/udev/rules.d/{rule.name}'
    print(cmd)
    subprocess.run(cmd.split(' '))
