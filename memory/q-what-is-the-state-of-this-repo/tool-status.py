#!/usr/bin/env python3
import subprocess
r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
print(r.stdout.strip() or "clean tree — nothing uncommitted")
