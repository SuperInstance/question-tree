#!/bin/bash
# demo.sh — the calculator maker, end to end.
# 1. Seed one question branch. 2. Turn the crank. 3. Meet a novel prompt:
#    no path -> BUILD the calculator (branch + tool + commit) -> answer through it.
# 4. Ask again -> now it's just crank-turning.
cd "$(dirname "$0")"
Q=./qtree.py

echo "=== 1. seed: grow the first question ==="
$Q grow "what is the state of this repo" --tool status <<'EOF'
#!/usr/bin/env python3
import subprocess
r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
print(r.stdout.strip() or "clean tree — nothing uncommitted")
EOF

echo
echo "=== 2. ask something the tree knows: turn the crank ==="
$Q ask "what is the repo status right now"

echo
echo "=== 3. ask something novel: no path -> build the calculator ==="
$Q ask "who changed the README last" || true

echo
echo "--- agent builds: new question branch + tool + commit ---"
$Q grow "who changed a file last" --tool blame <<'EOF'
#!/usr/bin/env python3
import subprocess, sys
target = sys.argv[1] if len(sys.argv) > 1 else "README.md"
r = subprocess.run(["git", "log", "-1", "--format=%h %an %ad %s", "--date=short", "--", target],
                   capture_output=True, text=True)
print(r.stdout.strip() or f"no history for {target}")
EOF

echo
echo "=== 4. ask again: now it's just crank-turning ==="
$Q ask "who changed the README last"

echo
echo "=== the tree ==="
$Q map
echo
echo "=== growth history (git log) ==="
$Q log
