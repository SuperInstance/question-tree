#!/usr/bin/env python3
import subprocess, sys
target = sys.argv[1] if len(sys.argv) > 1 else "README.md"
r = subprocess.run(["git", "log", "-1", "--format=%h %an %ad %s", "--date=short", "--", target],
                   capture_output=True, text=True)
print(r.stdout.strip() or f"no history for {target}")
