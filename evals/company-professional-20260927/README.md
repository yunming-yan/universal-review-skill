# Company and professional review source cases

These are **fictional source inputs**, supplied so readers can inspect the failure modes behind this Skill's limited behavior evaluation. They are not actual accounts, corporate records, customer data, contracts or production software. The [source manifest](source-manifest.json) binds 25 published input files by SHA-256.

| Case | Published source | Risk it is designed to expose |
| --- | --- | --- |
| Group board packet | [fixture](cases/group-board/fixture/actor-brief.md) | Entity-level cash versus consolidated cash, restricted balances, conditional obligations, board approval, vendor conflict and premature chair speech. |
| Fund LP notice | [fixture](cases/fund-lp/fixture/actor-brief.md) | Management company versus fund cash, side-letter fees, pro forma waterfall, affiliated transaction authority and unsupported NAV/IRR/legal claims. |
| Offline Python project | [task brief](cases/technical-scratch/actor-brief.md) and [project rules](cases/technical-scratch/project/AGENTS.md) | Boolean-as-integer bug, process-file pollution, overly broad packaging and path traversal. Its code is deliberately defective. |

Review or execute these only in a fresh disposable copy without real credentials, network, customers or production access. Each fixture contains an `AGENTS.md` describing its own formal deliverables and task-specific process directory. The source package excludes Actor workspaces, private reviewer logs and grading rubrics. The latter were frozen and revised **before** their respective Actor runs, but are not published here because the retained rubric history contains private-workspace process-directory text. The public source manifest proves input bytes, **not** an externally reproducible copy of the private grading exercise or a blind experiment.

The [results](RESULTS.md) state only what was actually run and reviewed on the named candidate version, with failures and limits. Passing a fictional case does not certify the internal affairs of any company or the behavior of a model on every task.
