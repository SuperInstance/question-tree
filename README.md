# question-tree

A memory system for a git agent, organized by **questions**, not answers.

## The inversion

Most memory systems are answer-side: store what was concluded, retrieve past
text that looks like the current prompt. This one is question-side:

- Every folder is a **question**.
- Inside a folder: deeper folders (finer questions) or **leaves**.
- A leaf is a **tool** that renders the last mile — or, rarely, a terminal answer.

## The discipline (the calculator maker)

When the agent is asked something, it does not think and answer. It:

1. **Walks** the tree — matches the prompt to a question path.
2. If a path exists, **turns the crank** — runs the leaf tool.
3. If no path exists, **builds the calculator first** — decomposes the prompt
   into questions, grows the branch, writes the tool, commits — then answers
   through it.

Answers give you one route: 8×8 → 64. A calculator answers anything,
*including* 8×8. Different animal.

## Why questions outlast answers

Answers rot — they depend on context that shifts. Questions are the stable
part: "what's the failure mode?", "who pays if this breaks?", "what changed
last?" survive across situations. And followed down far enough, questions
stop yielding facts and start yielding **capabilities**. The tree compiles
into tools. The inquiry is the durable structure; answers were just the last
mile being rendered.

Like the bathymetric recorder: the charts get accurate in the anchorages and
passages travelled most. The most-walked branches get the most refined tools.

## Git is the growth record

Every grown branch is a commit: `q: <question>`. The log reads as the history
of the agent's curiosity. Branches can be refined, reverted, merged — the
memory has version control because it *is* a repo.

## Layout

```
memory/
  q-<slug>/              a question
    question.md          the question in full prose
    README.md            written by the agent, for the agent: what's here
    q-<slug>/            a finer question
    tool-<name>.py       executable leaf — renders the last mile
    answer.md            terminal answer leaf (rare)
```

## Demo

```bash
./demo.sh
```

Seeds one branch, turns the crank on it, then meets a novel prompt: no path,
so the agent builds the calculator (new branch + tool + commit) and answers
through it. Ask again — now it's just crank-turning.
