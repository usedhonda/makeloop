# Project Instructions

## Project Notes

- Keep repository-specific runbooks, sharp edges, and operating decisions in `CLAUDE.md`.
- Keep longer implementation notes and external AI discussions under `docs/`.
- Let bootstrap-managed blocks stay machine-owned; edit the user-authored sections around them.

## Git workflow

- Interactive changes (human or agent) go through a feature branch and a pull request to `main`; never push directly to `main`.
- Sole exception: the self-improvement cron's deterministic wrapper (Tier-1 auto-push after gate PASS; see `plugins/makeloop/AUTOMATION.md`), which remains a sanctioned direct push.
- Never force-push. If a push or merge fails, keep the commits local and report to a human.
