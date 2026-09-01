# Claude Code Agents & Workflows: The Basics

A plain-language guide to the three building blocks you'll use most as a
beginner: subagents, slash commands/skills, and multi-step workflows.

## What do "agent" and "workflow" even mean here?

An **agent** is just Claude, given a specific job and (sometimes) its own
set of instructions and tools, so it behaves more like a specialist than a
generalist. Instead of you re-explaining "review this code like a security
expert would" every time, you write that instruction down once and Claude
can reuse it.

A **workflow** is a sequence of steps toward a bigger goal — research,
then draft, then review, for example. You can run a workflow just by
prompting Claude through the steps in one conversation, or you can save
the sequence so it's repeatable.

Everything below is a different way of packaging "instructions you don't
want to retype."

---

## 1. Subagents

**What they are:** A subagent is a specialized helper with its own name,
its own instructions, and (optionally) its own restricted set of tools.
Claude Code can hand a task off to one when the task matches what that
subagent is built for. Subagents live as markdown files in a folder
called `.claude/agents/`.

**When to use one:** When you have a narrow, repeatable job — something
you'd otherwise describe the same way every time. Examples: a "code
reviewer" that always checks for the same kinds of bugs, or a "research
summarizer" that always condenses sources the same way.

**Minimal example** — `.claude/agents/summarizer.md`:

```markdown
---
name: summarizer
description: Summarizes long text into 3 bullet points. Use when the user pastes an article or long document and asks for a summary.
tools: Read
---

Summarize the given text into exactly 3 bullet points. Keep each bullet
under 20 words. No preamble, no extra commentary.
```

Line by line:
- The block between `---` lines is called **frontmatter** — metadata
  that tells Claude Code about the subagent before it reads the
  instructions.
- `name` is the identifier used to invoke it.
- `description` tells Claude *when* to reach for this subagent — write it
  like a trigger condition, not a title.
- `tools` restricts what the subagent is allowed to use (here, just
  reading files — no editing, no running commands). Omit it to allow all
  tools.
- Everything below the second `---` is the actual instruction Claude
  follows when acting as this subagent.

---

## 2. Slash commands & skills

**What they are:** Both let you save a reusable instruction and trigger
it by typing `/name` instead of retyping the whole prompt.

**The difference in one sentence:** a **slash command** is a saved
prompt (a fixed set of instructions you invoke on demand); a **skill** is
a packaged set of instructions Claude can also load automatically when it
notices your task matches, without you typing a command at all.

**Minimal example** — a custom slash command at
`.claude/commands/standup.md`:

```markdown
Summarize what I worked on today based on my recent file edits and git
commits, formatted as 3 short bullet points for a standup update.
```

Typing `/standup` runs exactly that prompt — no retyping required.

---

## 3. Multi-step workflows

**What they are:** Chaining several steps together toward one outcome,
instead of doing each step as a separate, disconnected ask. You can do
this two ways:
- **Ad hoc:** just prompt Claude through the steps in one conversation
  ("first research X, then draft a summary, then check it for errors").
- **Saved:** wire the same sequence into a slash command or skill so it
  repeats identically every time.

**Walk-through example — a generic 3-step research workflow:**

1. **Research:** "Look into [topic] and list the 5 most relevant
   points."
2. **Draft:** "Turn those 5 points into a short summary a beginner could
   understand."
3. **Review:** "Check the summary for anything inaccurate or unclear, and
   fix it."

Each step feeds the next. Once you've done this manually a few times and
like the result, that's your cue to save it as a slash command so you
don't have to describe the steps again.

---

## Quick comparison

| Building block  | What it is                                   | Triggered by                          |
|------------------|-----------------------------------------------|----------------------------------------|
| Subagent         | A specialist with its own instructions/tools  | Claude delegating a matching task      |
| Slash command    | A saved, fixed prompt                         | You typing `/name`                     |
| Skill            | A packaged instruction set                    | You typing `/name`, or Claude noticing a match automatically |
| Workflow         | A sequence of steps toward one goal           | You, prompting through the steps (or a saved command/skill running them) |

---

## Suggested next step

Try creating one simple subagent in this workspace — something you'd
actually reuse, like a "resource summarizer" for the `/resources` folder.
Start small: a name, a one-sentence description, and 2-3 sentences of
instructions. You can always add more later.
