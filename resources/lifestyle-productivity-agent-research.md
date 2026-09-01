# Lifestyle, Personal Assistant & Productivity Agents: Research Deep Dive

Research pass on real, working examples of "Jarvis-style" assistants and
productivity agents — ones you can realistically build or set up yourself,
not just concepts. Covers three lanes: **Claude-native** (subagents, skills,
connectors), **no-code automation** (n8n, Zapier), and **standalone apps**
(SaaS tools with their own connectors). Each entry has what it does, how
hard it is to set up, and what it connects to.

"Jarvis-feel" note: the entries marked 🦾 are the ones that get closest to
"talk to it, it handles things across your apps" — those all require
connecting at least one outside service (calendar, email, Telegram, etc.).
Everything else works standalone, no connectors needed.

---

## Claude-native (build inside this workspace or Claude directly)

### 1. Habit Check-In Subagent — *you already have this one*
**What it does:** A Claude Code subagent (`dolly` in this workspace) that
runs your daily check-in and tracks streaks for workouts, meditation, yoga,
sleep, etc.
**Difficulty:** Already built — see `dolly-agent/` in this workspace.
**Connectors:** None — pure conversation + local file storage.
**Why it's on this list:** Proof this whole category is realistic. You
already built a working example of it.

### 2. Anthropic's Official Productivity Skills/Plugins 🦾
**What it does:** Anthropic ships an official plugin bundle for Claude
Cowork/Claude Code covering document handling (PDF/PPTX/XLSX/DOCX),
memory maintenance (`consolidate-memory`), skill authoring, and
**scheduling** — `/start` initializes tasks, memory, and a visual
dashboard; `/update` triages stale items and memory gaps.
**Difficulty:** Easy. One CLI command:
```
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install <plugin-name>@knowledge-work-plugins
```
**Connectors:** Built-in memory/scheduling tools; some plugins add
Google Workspace access.
**Guide:** [GitHub – anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [Use plugins in Claude – Anthropic Help Center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)

### 3. Claude + Google Workspace Connectors (Gmail, Calendar, Drive) 🦾
**What it does:** Turns on native Claude access to your Gmail, Google
Calendar, and Google Drive — Claude can read your inbox, check/create
calendar events, and pull files into a conversation, all through toggle-on
connectors (no separate server to run). This is what already powers
Gmail/Calendar/Drive access in this very session.
**Difficulty:** Easy — it's a toggle in Claude settings, not a build.
Read/write on Calendar; Gmail is send-only with your approval (nothing
fires automatically on new mail yet).
**Connectors:** Gmail, Google Calendar, Google Drive (official Anthropic
connectors).
**Guide:** [Use Google Workspace connectors – Anthropic Help Center](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)

### 4. DIY "Jarvis" Built on Claude Code
**What it does:** A from-scratch personal assistant built using Claude
Code as the brain — plans your day, manages projects, processes email, and
remembers how you work over time. Useful as an architecture reference: a
personal AI assistant is generally four layers — an **interface** (how you
talk to it), an **orchestrator** (routes requests), **tool/integration**
(calendar, email, etc.), and **memory** (remembers your preferences).
**Difficulty:** Medium — this is a multi-session project, not a
one-sitting build. Realistic expectations: ~2 weeks for a basic read-only
assistant, ~6 weeks to get it drafting things for your approval.
**Connectors:** Whatever you wire in — typically email + calendar first.
**Guide:** [How to Build a Jarvis AI Assistant With Claude Code](https://sidbharath.com/blog/how-i-built-jarvis/)

---

## No-code automation (n8n / Zapier — drag-and-drop, no programming)

### 5. "Jarvis" Productivity Agent Template (n8n) 🦾
**What it does:** Literally named Jarvis — a Telegram-based hub where you
message tasks, calendar changes, emails, or expenses in plain text (or
voice), and it routes each one to the right tool via MCP (tasks, calendar,
email, expense tracking all in one chat thread).
**Difficulty:** Medium — free n8n account, import the template, connect
your accounts (Telegram bot token, Google Calendar, Gmail, etc.) and add
an OpenAI/Claude API key. No coding, but real setup time (30–60 min).
**Connectors:** Telegram, Google Calendar, Gmail, expense tracking.
**Guide:** [n8n – Jarvis: productivity AI agent for tasks, calendar, email & expense using MCPs](https://n8n.io/workflows/8500-jarvis-productivity-ai-agent-for-tasks-calendar-email-and-expense-using-mcps/)

### 6. Telegram Personal Assistant (Tasks, Email & Calendar) 🦾
**What it does:** Similar idea to #5 but built around GPT-4o — text or
voice-message a Telegram bot, it transcribes voice notes, remembers
context, and manages tasks/email/calendar for you.
**Difficulty:** Medium — same n8n import-and-connect process as above.
Good second option if you want to compare templates before picking one.
**Connectors:** Telegram, Gmail, Google Calendar.
**Guide:** [n8n – Manage Tasks, Email & Calendar with GPT-4o Personal Assistant on Telegram](https://n8n.io/workflows/8695-manage-tasks-email-and-calendar-with-gpt-4o-personal-assistant-on-telegram/)

### 7. Habit Tracking Automations (Zapier) 🦾
**What it does:** Pre-built "Zaps" that log habits automatically — e.g.
a form submission or app entry triggers a log row in a spreadsheet, or a
daily reminder pings you to check in.
**Difficulty:** Easy — Zapier's whole pitch is natural-language setup;
pick a template, connect the two apps, done.
**Connectors:** Depends on the template — commonly Google Sheets, Slack,
reminder/calendar apps.
**Guide:** [Zapier – Habit Tracking Automations & AI Workflows](https://zapier.com/automations/personal-productivity/health-wellness-tracking/habit-tracking)

---

## Standalone apps (SaaS, own connectors, no building required)

### 8. Reclaim.ai 🦾
**What it does:** Auto-schedules your habits (workouts, focus time,
meals) directly onto your Google Calendar and defends the time blocks by
marking them busy. You set preferences once ("mornings are my focus
time") and it works in the background from then on.
**Difficulty:** Easy — sign up, connect Google Calendar, add your
task manager (Todoist, Asana, ClickUp, or Jira). Genuinely "set and
forget," unlike Motion which has a steeper setup curve.
**Connectors:** Google Calendar (required), Todoist/Asana/ClickUp/Jira
(optional, for task sync).
**Guide:** [reclaim.ai](https://reclaim.ai/) — free tier covers basic habit + task scheduling.

### 9. Teal / Huntr (Job Search Tracker)
**What it does:** Keeps every job application organized in one place —
status, dates, notes, follow-up reminders — instead of a spreadsheet.
Directly useful given you're actively applying.
**Difficulty:** Easy — sign up, install the browser extension, it
autofills tracker entries as you apply.
**Connectors:** Browser extension only (captures job postings as you
browse); no email/calendar wiring needed.
**Guide:** [Teal](https://www.tealhq.com/) · [Huntr](https://huntr.co/)

### 10. Tsenta (AI Job-Application Agent) 🦾
**What it does:** A step up from a tracker — this one actually applies
for you. It watches company career pages, matches roles to your resume,
fills out the application (including open-ended questions, in your own
voice), and shows you a diff to approve before anything gets submitted.
**Difficulty:** Medium — upload your resume, set your job criteria,
review its first few applications closely before trusting it to move
faster. Human-in-the-loop by design, so it's not "fire and forget."
**Connectors:** Browser extension + ATS (applicant tracking system) sites
directly.
**Guide:** [tsenta.com](https://tsenta.com/)

---

## Quick comparison

| # | Agent | Category | Difficulty | Connectors | Jarvis-feel |
|---|-------|----------|------------|------------|:---:|
| 1 | Habit Check-In (Dolly) | Claude subagent | Done already | None | |
| 2 | Anthropic productivity plugins | Claude Cowork | Easy | Built-in | 🦾 |
| 3 | Claude Google Workspace connectors | Claude native | Easy | Gmail/Calendar/Drive | 🦾 |
| 4 | DIY Jarvis on Claude Code | Claude Code project | Medium | Whatever you wire in | 🦾 |
| 5 | n8n "Jarvis" MCP template | No-code | Medium | Telegram, Calendar, Gmail | 🦾 |
| 6 | n8n Telegram GPT-4o assistant | No-code | Medium | Telegram, Gmail, Calendar | 🦾 |
| 7 | Zapier habit automations | No-code | Easy | Varies | 🦾 |
| 8 | Reclaim.ai | SaaS app | Easy | Google Calendar, task apps | 🦾 |
| 9 | Teal / Huntr | SaaS app | Easy | Browser extension | |
| 10 | Tsenta | SaaS agent | Medium | Browser + ATS sites | 🦾 |

---

## Where to start

**If you want the "Jarvis" feeling with the least setup:** start with #3
(Claude's Google Workspace connectors) — you already have Gmail and
Calendar access in this very session, so there's nothing left to build,
just prompts to try (e.g. "what's on my calendar today, and draft a reply
to the last email from X").

**If you want to actually build something:** #1 (which you've already
done) proves the pattern works. A natural next build using that same
approach would be the **Inbox Triage Agent** or **Job Application
Follow-Up Agent** from `resources/productivity-agent-ideas.md`, now that
you have real Gmail access to wire it into.

**If you want the full "talk to it, it handles everything" experience:**
#5 or #6 (n8n templates) get you closest, but budget an afternoon for
setup — connecting accounts and API keys is the real work, not the
no-code part.

---

## Sources

- [Best Claude Code Subagents and Custom Agent Examples in 2026](https://promptessor.com/blog/best-claude-code-subagents-and-custom-agent-examples-for-specialized-coding-workflows-in-2026)
- [GitHub – anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- [Use plugins in Claude – Anthropic Help Center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Use Google Workspace connectors – Anthropic Help Center](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Google Calendar MCP Integration with Claude Code – Composio](https://composio.dev/toolkits/googlecalendar/framework/claude-code)
- [How to Build a Jarvis AI Assistant With Claude Code](https://sidbharath.com/blog/how-i-built-jarvis/)
- [Building Your Own Jarvis: Personal AI Assistant Architecture in 2026](https://eucalipse.com/articles/build-your-own-jarvis-personal-ai-assistant)
- [n8n – Jarvis: productivity AI agent for tasks, calendar, email & expense using MCPs](https://n8n.io/workflows/8500-jarvis-productivity-ai-agent-for-tasks-calendar-email-and-expense-using-mcps/)
- [n8n – Manage Tasks, Email & Calendar with GPT-4o Personal Assistant on Telegram](https://n8n.io/workflows/8695-manage-tasks-email-and-calendar-with-gpt-4o-personal-assistant-on-telegram/)
- [Zapier – Habit Tracking Automations & AI Workflows](https://zapier.com/automations/personal-productivity/health-wellness-tracking/habit-tracking)
- [Sunsama vs Reclaim.ai: feature-by-feature comparison for 2026 – Reclaim](https://reclaim.ai/blog/sunsama-vs-reclaim)
- [Top-Rated AI Job Search Agents and Automation Tools 2026 – Tsenta](https://tsenta.com/blog/top-rated-ai-job-search-agents-automation-tools)
- [Tsenta AI Job Search Agent](https://tsenta.com/)
- [OpenJarvis – Personal AI, On Personal Devices (GitHub)](https://github.com/open-jarvis/OpenJarvis)
