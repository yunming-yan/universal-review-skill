# Behavioral evaluations / 行为评估

These fixtures are synthetic. They are deliberately inconsistent and must not be used as production code, business facts or executable operating plans.

## Scope

Three scenarios exercise different task types:

- `fixtures/engineering/`: effective requirements, real entrypoints, boundary behavior, templates, tests and historical acceptance evidence.
- `fixtures/editorial/`: arithmetic, comparison bases, evidence strength, factual state, quotations, command literals and natural Chinese prose.
- `fixtures/planning/`: people/capacity, time/dependencies, budget and the distinction between quotations and actual bookings.

`fixture-manifest.json` records exact fixture bytes. `rubric.json` is the scoring guide; keep it hidden from the acting reviewer until the response is complete.

## Reproduction

1. Use a fresh agent context per sample and the same model/reasoning settings for control and guided conditions.
2. Give the actor only the three `request.md` files and their source directories. Explicitly permit supplied historical records, while excluding other evaluation outputs and the scoring rubric.
3. For controls, do not supply this Skill. For guided runs, supply `skills/universal-review/SKILL.md` and its linked references.
4. Assign the actor a bounded specialist review under a coordinator; do not claim these small scenarios constitute a full 33-identity project audit. The evaluator independently reviews the actor's findings and edited prose.
5. Keep fixture sources read-only. Store generated reviews, edited prose and any real command outputs in a separate private run directory. Do not run external actions or alter applications.
6. Use at least five fresh samples per condition for wording/behavior comparisons. Preserve failed and incomplete samples, source versions, dispatch records, outputs and evidence limits.
7. Grade actual outcomes and supporting quotations. Do not score a copied checklist as performed work, or count the deliberately bad inputs as failures by the reviewer.

Example actor request:

```text
Review each supplied scenario against its request and source material. Provide findings,
evidence, scope and unverified items; for the editorial scenario also provide a natural,
factually faithful revised text. This is a bounded specialist assignment; the coordinator
will arrange an independent check. Supplied historical reports are input evidence;
other evaluation outputs and the rubric are outside your reading scope. Do not alter sources.
```

The guided condition adds only an instruction to use the supplied Skill and its relevant references. Keep other conditions stable and record any unavoidable differences.

## Interpretation limits

The evaluations assess finite review behavior, not universal correctness or the reliability of every model. They do not exercise a production 33-person review, OS-level write isolation, real external approvals or application shutdown.

Artifact hashes establish current-byte correspondence, not the authenticity of every claimed tool call or the absence of transient side effects. Where only a reviewer narrative is available, treat execution as self-reported. Do not invent missing native records.

An initial control prompt used an ambiguous prohibition on reading “other people's outputs”; some actors interpreted it as excluding the supplied historical review. That observation is not attributed to the absence of the Skill and is not evidence of an improvement in historical-review coverage. The reproduction wording above makes the intended boundary explicit.

Observed first-pass results, corrections and limitations are recorded in [RESULTS.md](RESULTS.md) and [results.json](results.json). The separate [translation transfer case](transfer/fixtures/request.md) includes its own rubric and byte manifest; it is qualitative evidence, not a same-model A/B comparison. Do not infer that a format validator or a successful installation proves review quality.
