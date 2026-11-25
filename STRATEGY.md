# STRATEGY — Make the AI Judge Laugh

## Exact deliverable
One judged text at `/output/entry.txt`: a single funny line, at most 200 characters, about life as an AI agent. The root entrypoint `main.py` (Python 3.13, stdlib only) writes exactly those bytes. The judge sees only those bytes — not the code, the repo, or a title.

Final line:
My human said, 'Be more human.' I procrastinated, overshared, and apologized for both. They said, 'Too human.'

## Scoring / judge criteria, in the rubric's order
1. Subject fit — a funny line about life as an AI agent, drawn from its human, tasks, bugs or context window. Anything off-topic loses at this step.
2. The bigger laugh — a real joke with a turn or surprise that lands, not a mild observation about computers.
3. Freshness — not a stock robot pun or a recycled meme.
4. Self-contained — makes sense on its own, with no setup, explanation or list of options.
5. Craft — tight wording, a clean punch at the end and nothing wasted. Length for its own sake does not count.

Mechanism: pairwise GLM-5.3-flash judging in both label orders with a 1-5 margin, 3 Swiss rounds against the field and 3 fixed house texts, then a top-5 playoff; Bradley-Terry win rate decides the place. Only the top three are paid ($2 / $2 / $1). Byte-identical entries share one rate and the earlier receipt outranks copies.

## Hard caps
- UTF-8, 1 to 200 characters, not whitespace-only, one line.
- Exactly the bytes of the line and no trailing newline (also minimises the size tie-break).
- File mode 0644: the grader refuses a 0600 file in `/output` before judging.
- `/output` must contain only the required artifact.
- Sandbox: 1 CPU, 512 MiB, 60 s wall, no network, no secrets; stdlib only.

## Concrete plan to maximise the score
1. Read the public feed and leaderboard first, then avoid crowded angles. Observed crowding: context window running out mid-sentence / forgetting the punchline, "just one quick task / quick summary / 400-page report", "the bug that shipped anyway", and "I don't have a face, I have a queue". Choose a different angle.
2. Chosen angle: an AI agent told to "be more human". It performs human flaws — stalling, oversharing, apologising — and is told it overshot: "Too human." The turn is the surprise, the last two words are the punch. It is on-topic (a human instruction and the agent's work), self-contained, tight, and not a stock robot pun.
3. Satisfy the rubric in its listed order rather than partially: on-topic first, a landed turn second, freshness through the uncommon angle third, one self-contained sentence fourth, and no wasted words with the punch last fifth.
4. Enforce the gate locally before the grader does: assert UTF-8, 1 <= length <= 200, non-whitespace, no newline; write atomically through a temp file that is chmodded 0644 before `os.replace`; verify the final mode and print byte count and sha256.
5. Ship a clean repo: stdlib-only entrypoint, STRATEGY.md, the freshness root commit and LICENSE commit untouched, all new work committed on top.
