#!/usr/bin/env python3
"""qtree — question-tree memory for a git agent.

The inversion: folders are QUESTIONS, not topics. Inside a folder you find
either deeper folders (finer questions) or leaves. A leaf is a TOOL that
renders the last mile — or, rarely, a terminal answer.

The agent's discipline: when asked something, never just answer. Walk the
tree. If a path exists, turn the crank (run the leaf tool). If no path
exists, BUILD the calculator first — decompose the prompt into questions,
grow the branch, write the tool, commit — and then answer through it.

Answers give you one route (8x8 -> 64). A calculator answers anything,
including 8x8. This is the calculator maker.

Usage:
    qtree.py ask "prompt"          walk the tree; run the leaf tool or report no-path
    qtree.py grow "question" --parent <q-slug> --tool <name>   scaffold a branch
                                               (tool code via stdin)
    qtree.py log                   show the growth history (git log of questions)
    qtree.py map                   print the whole question tree

Matching is deliberate token overlap — deterministic, no API, no magic.
A POC-grade matcher for a POC-grade memory. Swap it later; the tree is the point.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join(HERE, "memory")
STOP = set("a an the is are was were be been do does did what who when where why how which whom whose this that these those it its of in on to for with and or as at by from".split())


def slug(q):
    s = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")
    return "q-" + s[:60].strip("-")


def tokens(s):
    return set(t for t in re.split(r"[^a-z0-9]+", s.lower()) if t and t not in STOP)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=HERE, **kw)


def questions():
    """All question folders: (slug, path, question-text)."""
    out = []
    for root, dirs, files in os.walk(MEM):
        if "question.md" in files:
            with open(os.path.join(root, "question.md")) as f:
                q = f.read().strip()
            out.append((os.path.basename(root), root, q))
    return out


def leaves(path):
    """Tool, skill, and answer leaves directly inside a question folder."""
    tools = sorted(f for f in os.listdir(path)
                   if f.startswith("tool-") and os.access(os.path.join(path, f), os.X_OK))
    skills = sorted(d for d in os.listdir(path)
                    if d.startswith("skill-") and os.path.isdir(os.path.join(path, d)))
    answers = sorted(f for f in os.listdir(path) if f == "answer.md")
    return tools, skills, answers


def score(prompt, question):
    pt, qt = tokens(prompt), tokens(question)
    if not qt:
        return 0
    return len(pt & qt) / len(qt)


def ask(prompt):
    qs = questions()
    if not qs:
        print("no-path: the tree is empty. grow the first question.")
        return 1
    ranked = sorted(((score(prompt, q), s, p, q) for s, p, q in qs), reverse=True)
    best, s, p, q = ranked[0]
    if best < 0.34:
        print(f"no-path: nothing close. closest was '{q}' (score {best:.2f}). grow it.")
        return 1
    tools, skills, answers = leaves(p)
    print(f"path: {s}/  (matched: \"{q}\"  score {best:.2f})")
    if skills:
        sk = skills[0]
        sm = os.path.join(p, sk, "SKILL.md")
        print(f"skill: {sk}/")
        if os.path.exists(sm):
            with open(sm) as f:
                print(f.read().strip()[:600])
        return 0
    if tools:
        t = tools[0]
        print(f"crank: running {t}")
        r = subprocess.run([os.path.join(p, t)], capture_output=True, text=True, cwd=HERE)
        print(r.stdout.strip() or "(tool produced no output)")
        if r.stderr.strip():
            print("(stderr) " + r.stderr.strip()[:200])
        return 0
    if answers:
        with open(os.path.join(p, answers[0])) as f:
            print("terminal answer:\n" + f.read().strip())
        return 0
    print("dead-end: question exists but has no tool and no sub-questions. grow deeper.")
    return 1


def grow(question, parent=None, tool=None):
    s = slug(question)
    base = os.path.join(MEM, parent) if parent else MEM
    if parent and not os.path.isdir(base):
        sys.exit(f"no such parent question folder: {parent}")
    path = os.path.join(base, s)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "question.md"), "w") as f:
        f.write(question.strip() + "\n")
    if tool:
        tool_path = os.path.join(path, f"tool-{tool}.py")
        code = sys.stdin.read()
        with open(tool_path, "w") as f:
            f.write(code)
        os.chmod(tool_path, 0o755)
    kids = [d for d in sorted(os.listdir(path)) if d.startswith("q-")]
    tools_here = sorted(t for t in os.listdir(path) if t.startswith("tool-"))
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write(f"# {question.strip()}\n\n")
        f.write("This folder is a question. Deeper folders are finer questions; "
                "tools at the leaves render the last mile.\n\n")
        f.write("## Sub-questions\n" + ("".join(f"- {k}/\n" for k in kids) or "(none yet)\n"))
        f.write("\n## Tools\n" + ("".join(f"- {t}\n" for t in tools_here) or "(none yet)\n"))
    run(["git", "add", "."])
    r = run(["git", "commit", "-q", "-m", f"q: {question.strip()}" + (f" [+tool-{tool}]" if tool else "")])
    print(f"grew: {os.path.relpath(path, MEM)}/" + (f" with tool-{tool}.py" if tool else ""))
    return 0


def map_tree():
    for root, dirs, files in os.walk(MEM):
        dirs.sort()
        depth = root.replace(MEM, "").count(os.sep)
        name = os.path.basename(root) or "memory"
        if "question.md" in files:
            with open(os.path.join(root, "question.md")) as f:
                q = f.read().strip()[:80]
            print("  " * depth + f"{name}/  — \"{q}\"")
        else:
            print("  " * depth + f"{name}/")
        for t in sorted(f for f in files if f.startswith("tool-")):
            print("  " * (depth + 1) + f"[{t}]")
        for d in sorted(d for d in dirs if d.startswith("skill-")):
            print("  " * (depth + 1) + f"[{d}/ skill]")
        for a in sorted(f for f in files if f == "answer.md"):
            print("  " * (depth + 1) + "[answer.md]")


def log():
    r = run(["git", "log", "--oneline", "--reverse"])
    print(r.stdout.strip() or "(no commits yet)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: qtree.py ask|grow|map|log ...")
    cmd = sys.argv[1]
    if cmd == "ask":
        sys.exit(ask(" ".join(sys.argv[2:])))
    elif cmd == "grow":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("question")
        ap.add_argument("--parent", default=None)
        ap.add_argument("--tool", default=None)
        a = ap.parse_args(sys.argv[2:])
        sys.exit(grow(a.question, a.parent, a.tool))
    elif cmd == "map":
        map_tree()
    elif cmd == "log":
        log()
    else:
        sys.exit(f"unknown command: {cmd}")
