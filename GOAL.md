# GOAL — StudyTrace

## The goal

By **Oct 30, 2026**, ship StudyTrace: a working, publicly demoable study assistant whose memory a student can fully see, question and control, built on **NVIDIA Nemotron via Nebius Token Factory**, and submitted to the **Personal AI** track.

**In one sentence for judges:**

> StudyTrace reads your Google Classroom, college email and notes, remembers what you've learned and what's due, and lets you trace every piece of advice back to the exact email, note or quiz it came from.

## Who it's for and the problem

College students juggling 5–7 courses miss deadline changes buried in email and don't have a clear picture of their weak topics. AI assistants that could help need to remember a lot about you, but their memory is a black box. StudyTrace makes that memory inspectable and correctable.

## Core features (must work end to end in the demo)

1. **Ingestion:** read-only Google Classroom (assignments, due dates, announcements, materials, grades) + course email + uploaded notes/PDFs become memories with sources.
2. **Memory timeline:** every memory shown with source, confidence, privacy tier and a Forget button.
3. **Conflict cards:** a rescheduled exam, a Classroom due date that disagrees with an email extension, or a fake "exam cancelled" email creates a conflict, not a silent overwrite.
4. **Study planner with "Why?":** "What should I study tonight?" returns a plan, and every item links to the memories and sources behind it.
5. **Quizzes that update memory:** quiz results visibly change confidence on weak/strong topic memories.
6. **Telegram companion:** deadline digest, study nudge and quizzes through Hermes Agent.

## Success criteria (how we know we're done)

### Ingestion and memory
- [ ] Seed inbox (~30 days of "Riya" emails) produces at least **35 correct memories**, each with a valid source quote.
- [ ] The demo Classroom (Riya's classes) syncs read-only: every assignment with a due date becomes a deadline memory linking back to Classroom, **with no model call**.
- [ ] Classroom announcements and attached materials produce memories through the same pipeline as email and notes.

### Conflicts and control
- [ ] A changed Classroom due date updates the deadline with a logged reason; a Classroom-vs-email date mismatch opens a conflict card citing both.
- [ ] The reschedule email and the fake cancellation email each open a conflict card.
- [ ] Every planner answer has at least one citation, and the Why view opens the original source.
- [ ] Forget removes a memory and changes the next plan; the same source doesn't re-create it.

### Models, privacy and infrastructure
- [ ] Nemotron **Nano handles the majority of model calls**; Super/Ultra only for reasoning, shown in a usage panel.
- [ ] **Zero `local_only` items** sent to any external API (shown in the outbound-call log).
- [ ] Nightly consolidation runs as a **Nebius Serverless Job**.

### Submission
- [ ] Hosted demo URL works with a seeded read-only account.
- [ ] Public repo with Apache-2.0 license, README (setup, Nemotron/Token Factory usage, feedback).
- [ ] Demo video under 3:00, public on YouTube.
- [ ] Submitted by **Oct 29 evening IST** (one day before the Oct 30, 10:30 pm IST deadline).

## Milestones

| Date | Milestone |
| --- | --- |
| Oct 12 | Public repo, skeleton, Postgres + pgvector in Docker, CI green; Token Factory key requested and Nemotron model IDs confirmed |
| Oct 14 | Token Factory, Hermes and sandbox running; seed data written; demo Classroom created with teacher and student accounts |
| Oct 19 | Classroom and email pipelines work end to end, with conflict detection |
| Oct 24 | **Feature freeze:** all six core features working |
| Oct 27 | Serverless job, privacy tiers, deployed demo |
| Oct 29 | Video recorded, README done, submitted |

## Non-goals (for this hackathon)

- Sending, replying to or modifying email.
- Writing to Google Classroom (turning in work, commenting, editing) or real-time push sync via Pub/Sub.
- Supporting non-student use cases or a general-purpose assistant.
- Multi-user accounts, sharing, or a mobile app.
- Fine-tuning or training models.
- Anything from the stretch list (weekly reflection, memory export, shared course memory, Hindi support) before the core is done.
