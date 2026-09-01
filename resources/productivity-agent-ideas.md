# Productivity Agent Ideas for Beginners

A shortlist of simple, useful subagents you could build in this workspace,
covering habits/health, everyday productivity, and email. Each one is
described conceptually — no code yet, just enough to help you pick one
worth building (the same way `resource-summarizer` came out of the
beginner's guide).

---

## 1. Daily Habit Check-In Agent

**What it does:** At the end of the day, you tell it what you did (worked
out, meditated, ate well, did yoga), and it keeps a running log — plus
tells you your current streak for each habit.

**Why it's useful:** Ties directly to your personal goals (working out,
eating healthy, meditation, yoga). Seeing a streak is a small nudge to
keep it going, and having Claude track it means you don't need a separate
habit-tracking app.

**When to reach for it:** Once a day, a quick "here's what I did today"
check-in.

---

## 2. Weekly Reflection Agent

**What it does:** Once a week, it looks back at whatever notes or
check-ins you've logged and summarizes: what went well, what slipped, and
one specific thing to try differently next week.

**Why it's useful:** Turns scattered daily notes into one clear takeaway,
without you having to reread everything yourself.

**When to reach for it:** Weekly, ideally paired with the Daily Habit
Check-In Agent above so it has something to reflect on.

---

## 3. Daily Priorities Agent

**What it does:** You dump your messy to-do list (however long or
disorganized), and it hands back your top 3 priorities for the day, with
a one-line reason for each.

**Why it's useful:** Cuts decision fatigue first thing in the morning —
instead of staring at 15 tasks, you get a short, actionable list.

**When to reach for it:** First thing in the morning, or whenever your
to-do list feels overwhelming.

---

## 4. Inbox Triage Agent

**What it does:** Reads through your unread or recent emails and sorts
them into three buckets — **needs a reply**, **FYI only**, and **can
ignore** — with a one-line summary of anything urgent.

**Why it's useful:** Email overload is one of the most common productivity
drains. This gives you a fast "what actually needs my attention" pass
instead of reading every email top to bottom.

**When to reach for it:** When your inbox has piled up and you want a
quick sort before diving in. (Note: this one would eventually need email
access set up and connected — worth building the *concept* now and
wiring up the connection later.)

---

## 5. Job Application Follow-Up Agent

**What it does:** You tell it which jobs you applied to and when, and it
reminds you which ones are due for a follow-up (e.g. no response after 1-2
weeks) and drafts a short, polite follow-up message for each.

**Why it's useful:** Job searching involves tracking a lot of moving
pieces — this keeps follow-ups from falling through the cracks without
you maintaining a spreadsheet by hand.

**When to reach for it:** Weekly, as part of a job-search routine.

---

## Picking one to build

Start with whichever one you'd actually use *today* — that's usually the
best sign it's worth building first. The Daily Habit Check-In Agent or
Daily Priorities Agent are the simplest starting points since they don't
depend on connecting anything external (like email).

Once you've picked one, we can build it the same way we built
`resource-summarizer`: a short description, a numbered set of steps, and
a plan for what it should reply with.
