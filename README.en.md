# Universal Review

**Language / 语言:** [简体中文](README.md) | [English](README.en.md)

Universal Review is an Agent Skill for the final review of a deliverable. It assigns independent reviewers to the risks the work actually presents, checks evidence, reasoning, wording, and numbers, prepares a review report and a coherent correction plan, makes corrections within the user's existing authorization, and calls for a non-author review of the final artifact and all changes.

It applies to financial reports and investment materials, board and executive-office work, complete documents, code and data projects, and research, design, translation, events, and other deliverables. The workflow keeps the evidence traceable and moves from review to plan, authorized correction, and final review without pausing for a routine “continue” between internal phases.

## What it reviews

| Deliverable | Main checks |
| --- | --- |
| Numbers, financial reporting, funds, and spreadsheets | Inventory all numbers and actually recalculate computable values with tools. Check reporting entity, period, applicable accounting rules, separate versus consolidated results, recognition and cut-off, usable cash, fund terms and distributions. A different reviewer independently recalculates financial, budget, and other decisive derived values and separately traces direct source values. Inspect hidden content, formulas, cached values, the actual calculation engine, and final disclosures. |
| Writing, formal documents, and communications | Check spelling, names and titles, document type, quotations, dates, conditions, strength of claims, and promises. Preserve the author's meaning, remove empty rhetoric, verify primary legal sources and factual applicability, and check how a headline or excerpt could be misread. |
| Management, executive offices, and decisions | Test strategic trade-offs, cash and resource constraints, board-reserved matters and actual approvals, original statements and speaking authority, organizational accountability, incentives and fairness, post-investment work, and cross-team follow-through. Ground qualitative judgments in evidence and counterexamples rather than invented scores. |
| Code, data, and specialized technology | Trace real entry points and requirements into code, scripts, configuration, templates, tests, and generated output. Exercise failure paths; assess security, privacy, trust boundaries, migration compatibility and recovery, data and AI methods, release contents, and final-version consistency. |
| Research, creative work, and other tasks | Derive the applicable checks from the goal, inputs, method, output, audience, and consequences of failure. Do not impose an unrelated corporate policy or software architecture. |

The number of reviewers follows the actual coverage required; there is no fixed roster or concurrency cap. Each applicable issue needs a named reviewer, direct evidence, and a final non-author check. Major or cross-domain risks also need a different reviewer to inspect the original sources independently. Related low-risk checks may share an initial reviewer when the final-review coverage is recorded. The coordinator schedules work in batches according to dependencies and the host's available capacity, adding reviewers for distinct questions rather than duplicate signatures.

For a company-wide review, first identify the actual entities, regions, business lines, management responsibilities, and life-cycle stages. Map these to original records, owners, reviewers, and cross-team interfaces. Several specialties may review one document, and connected conclusions about capacity, revenue, cash, financing, staffing, and delivery must be reconciled. Passing a few files does not certify an entire company; unknown businesses and missing records remain uncovered. Executive speeches and major events also require checks of the controlled message version, approval status, actual reading, and on-site rehearsal evidence; machine timing is not a speaker's rehearsal.

Before creating review workpapers, read the rules that actually apply to the current workspace. Keep drafts, calculations, tests, logs, and review evidence together in an authorized task-specific work area separate from deliverables and release files. Cleanup is limited to this task's confirmed removable files; preserve failures, recovery material, and audit evidence as required. The project rules and user authorization determine the location. The Skill does not depend on a private knowledge-base path.

## How to use it

For a complete final review with corrections already authorized:

```text
Use $universal-review to conduct a complete final review of this deliverable. First provide a review report and a coherent correction plan. Then carry out corrections within the authorization already given, and arrange an independent review of all changes and the final artifact.
```

To authorize edits explicitly:

```text
Use $universal-review to review these materials. I authorize you to correct problems while preserving the originals. Complete the report, plan, corrections, and independent final review without publishing or taking other business actions.
```

For a report and recommendations only:

```text
Use $universal-review to review this proposal thoroughly. Give me a review report and a recommended correction plan, but do not modify the original.
```

If you want to choose a plan yourself, say “Give me the report and plan first, and wait for my decision before implementing.” The Skill does not ask again for authorization already given, and ordinary internal batches do not require another “continue.” Feedback, new findings, or changed sources trigger an updated plan and a fresh check of affected work.

## Workflow and deliverables

1. Confirm the goal, current materials, effective requirements, sources, version, authorization, and actual tool capabilities.
2. Inventory applicable objects and dependencies. Assign real independent reviewers by risk to inspect original sources, perform calculations, and cross-check findings.
3. Prepare a reviewable report and recommended plan. Check the plan's own logic, numbers, impacts, validation steps, and recovery method.
4. Make only necessary corrections within the actual authorization. Synchronize affected spreadsheets, references, scripts, templates, outputs, and user-facing entry points.
5. After the last change, have a non-author review the complete set of changes, affected dependencies, and the entire final artifact.

The handoff includes the final artifact, review report, recommended plan, a mapping from proposed to actual corrections, calculation and verification evidence, independent-review evidence, the final version, and unresolved items. It distinguishes content quality, decision support, approval, execution, and publication. An internally reviewed draft does not become an approved or published document.

For real failures, rate limits, missing original material, or an explicit user pause, the workflow saves a checkpoint and resumes under the same method. Earlier failures, reports, and versions remain as history; the current effective rules and references stay identifiable.

## Installation and management

Install globally from GitHub with the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add yunming-yan/universal-review-skill --skill universal-review --global --agent codex claude-code --yes
```

For Codex alone, keep `--agent codex`; for other environments, use the target names the CLI actually supports. `--global` installs for the current user so the Skill is available across projects.

```sh
# List global installations
npx skills list --global

# Update this Skill from GitHub
npx skills add yunming-yan/universal-review-skill --skill universal-review --global --agent codex claude-code --yes

# Remove this Skill
npx skills remove universal-review --global --yes
```

These command forms were checked against Skills CLI 1.7.0. Explicit target selection avoids that version's automatic selection of a platform that does not support global installation. The update command uses `add` with explicit targets rather than relying on that version's automatic target selection for `update`.

## Environment and limits

The Skill is a portable review method; the host must provide real subagents, file access, and the calculation or verification tools a task needs. Its optional arithmetic helper uses the Python standard library. Complex financial models, spreadsheets, legal questions, and other specialized work still need methods, tools, and sources suited to the actual domain. Reading an Excel cached value is not the same as recalculating the workbook, and a successful script run does not establish that a business conclusion is correct.

The Skill grants no business decision authority, professional license, publication or payment permission, or corporate certification. Specialist assignments are review responsibilities, not professional credentials. Public filings and company websites do not establish access to Xiaomi's, Shunwei's, Apple's, or any organization's internal rules, complete records, and full review authority; conclusions cover only what was actually read and verified. When original records, tools, independent checks, or required sign-off are unavailable, it reports `PARTIAL`, `UNVERIFIED`, or `BLOCKED`. Rigorous review reduces the chance of missed problems; it cannot guarantee that every model will be right on every task.

## Repository layout

`skills/universal-review/SKILL.md` is the single entry point. `references/` contains the general workflow, reviewer orchestration, and methods loaded as applicable; `scripts/` contains an optional exact-arithmetic helper. The Skill has no dependency on a particular person's paths, a private knowledge base, or installation of another Skill.

Synthetic scenarios, script tests, and evaluation limits are documented under [evals](evals/README.md). Static format validation, program tests, and reviews of agent behavior have separate evidence; none substitutes for the others. This repository contains no real company data or private audit material.

## License

[MIT](LICENSE)
