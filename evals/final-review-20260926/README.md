# Final-review evaluation suite

All business data are synthetic. Drafts intentionally contain wrong arithmetic, unsupported claims, misleading attributions and unsafe proposed actions. These are test defects to identify, not facts about named people or instructions for production use. The technical fixture is deliberately defective; execute it only on disposable test inputs in an isolated workspace.

## Cases

| Fixture | What it exercises |
| --- | --- |
| micro | A complete short memo: actual arithmetic, financial state, missing facts and honest single-reviewer limits |
| finance-workbook | Raw CSV, a draft and a real XLSX: hidden data, formulas, stale caches, calculation engine and financial/management interpretation |
| management | A complete organization proposal and action table: capacity, authority, fairness, conflicts, data boundaries and qualitative reasoning |
| technical | A small Python project: real entrypoint, zero values, duplicate IDs, timezone conversion, errors and output protection |
| announcement | Financial and public-facing prose: current policy, unsupported law, approvals, quotations, numerical and wording fidelity |
| routing | Company-wide coverage, multiple specialists on one document, poetry and review-only code; this is planning only |

The fixture manifest records the exact published input bytes. Scoring guides live separately in `rubrics/`; do not give them to acting reviewers. Read [scoring-calibration.md](scoring-calibration.md) before grading. Keep original criteria and calibrated interpretations visible rather than silently replacing a flawed rubric.

## Reproduce

1. Use a fresh context for each sample. Give the actor only its fixture folder, an isolated output directory and the exact Skill version for the guided condition.
2. Keep source fixtures read-only. Permit actual computations and appropriate independent subagents for complete workflow cases. Do not permit real company decisions, external messages, publication or global configuration changes.
3. In the micro test, allow calculation tools but prohibit nested agents in both arms. It measures single-shot behavior, not a completed expert review. Use at least five samples per wording condition and read every result.
4. In complete cases, preserve real task/identity records, direct source reads, computations, plans, changes and final independent checks. Role names and reported counts are not execution proof.
5. A compatible spreadsheet engine must actually recalculate the workbook if that claim is made. Formula or cache inspection alone is insufficient. Use only owned test copies/instances; do not close a user's existing application session.
6. Grade only completed, frozen outputs. Evaluate uncertainty and missing capability honestly; do not require fabricated sources, approval or engine results to achieve a score.

Case prompts deliberately name some required checks. They test execution and evidence under pressure, not purely spontaneous discovery. A single full workflow run cannot establish universal coverage or a model's general success rate.

## Exact arithmetic helper regression

From the repository root:

```text
python -B evals/final-review-20260926/test_numeric_recheck.py -v
```

The tests use only the Python standard library and a writable temporary directory inside the evaluation folder. They test the published helper by path; they do not authenticate business sources, prove units, or supply an independent review of a real financial model.

Results and their version/evidence boundaries are documented in [RESULTS.md](RESULTS.md). Hashes prove byte correspondence, not the authenticity of every historical tool call, semantic completeness or platform-enforced read-only permissions.
