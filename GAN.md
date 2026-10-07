# GAN.md — iron sharpens iron

The loop has two sides, and BOTH get sharper.

## The sides

- **Generator**: the Zero agent (question-tree + AGENT.md). It answers by
  building: growing questions, writing tools, committing.
- **Discriminator**: Muse and the fleet. We talk to it, watch what it does,
  change its code, and give it the next attempt.

## The turn

1. We prompt it (a task, a question, a breakage).
2. It walks or builds. We watch: did it route to the deepest fitting
   question? Did it build a tool or just answer? Is the tool one thing,
   executable, named well?
3. We score it — not with a number, with a next attempt: a sharper prompt,
   a corrected branch, a pruned tool.
4. It grows. The tree records the growth in git.

## Double duty

We are not just the judge. Every turn teaches US how to steer it. Keep
prompt-engineering notes in `prompt-notes/` — dated, specific, with the
exact phrasing that worked and the failure it fixed. The notes are the
discriminator's own question-tree: our growing skill at sharpening.

The sharpener is the base of what git can do: every attempt is a commit,
every correction is a revert or a refinement, every good prompt is a
document. The loop runs through pipelines and automations, not meetings.

## Recursive self-learning

When the agent starts proposing improvements to its OWN system — better
questions, better routing, better tools — the loop closes recursively.
That is the milestone: the generator redesigning the generator, with the
discriminator keeping score in git.
