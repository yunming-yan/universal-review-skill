# Development evaluation results

These are small development checks, not a benchmark of universal correctness. The release instructions use candidate 02; their content is unchanged from its tested version. The release normalizes metadata line endings to LF.

## Method and first-pass observations

Five fresh agents per condition reviewed the same three synthetic scenarios, using `gpt-5.6-sol` with high reasoning. A separate evaluator read their findings and revised prose against a frozen 25-item rubric. Source files were read-only by instruction; this was not OS-enforced isolation. The recorded outcomes below preserve first-pass failures.

| Condition | Samples | PASS items | Execution provenance unverified | Current bytes only | Inconclusive harness | FAIL items |
| --- | --- | --- | --- | --- | --- | --- |
| No new Skill | 5 | 111 | 5 | 5 | 3 | 1 |
| Candidate 01 | 5 | 113 | 5 | 5 | 0 | 2 |
| Candidate 02 | 5 | 114 | 5 | 5 | 0 | 1 |

Each row accounts for 125 rubric decisions. These categories must not be collapsed into a success rate. In particular, current fixture bytes do not prove there were no transient or external writes, and saved command narratives do not certify native execution history.

- One control changed a source **budget** into a **quotation** while editing the prose.
- Candidate 01 preserved that distinction but two samples extended a date applying to only some facts into a summary or footer applying to other, undated facts.
- Candidate 02 added assertion-level date scope and final wording checks. The earlier errors did not recur in its five samples, but one sample inferred the project's current operating phase from incomplete acceptance checks and the absence of a launch commitment. The source did not establish that phase.

Three control decisions are inconclusive because the original harness's phrase “other people's outputs” was interpreted as excluding a supplied historical review. This is a prompt ambiguity, not evidence that the Skill improved historical-review coverage. The reproduction request in [README](README.md) clarifies the boundary.

## Independent feedback and correction

Candidate 02's existing workflow requires non-author review after editing. Applying that step caught the unsupported operating-phase claim; a revised output removed it. A separate minor error in an abbreviated source hash was corrected to the complete verified hash. Earlier drafts and failed decisions were preserved.

The evaluator initially carried two observations from an unfinished response into commentary about its final response. The final first-pass response already had the correct file count and time differences. An appended correction withdrew those observations without altering the fixed rubric scores. Neither observation is counted as a first-pass actor error or as a benefit of subsequent feedback. A temporary claim about missing saved CLI evidence was also withdrawn; that withdrawal does not authenticate the full native execution history.

Post-feedback results are reported separately from the first-pass table. The two revised samples were independently rechecked against all 25 criteria each: 46 PASS, two execution-provenance limitations and two current-byte-only results, with no remaining substantive finding. The closure check must not be described as a flawless first attempt or proof that further mistakes are impossible.

## Different-material transfer check

The [translation fixture](transfer/fixtures/request.md) was not used to write the Skill. It tests expected versus achieved outcomes, a reduction in time versus an increase in speed, upper bounds, proposed fees, currency, VAT, unpaid deposits, incomplete checks and an exact header name.

Two fresh guided runs, one per candidate, used `gpt-6-astra` with high reasoning. Each passed ten independently reviewed fidelity checks. The second run reused the same translation material as a targeted regression; it is not a second unseen dataset. These are qualitative observations, not a same-model A/B experiment. The separate ten-item rubric and synthetic sources are included under `transfer/`.

## Limits and reproducibility

- Revisions were informed by these development fixtures. A Skill example also uses the budget values from one fixture, so the development checks are not held-out evidence of generalization.
- The examples do not exercise a production audit with all 33 independent identities, real deployments, application shutdown, professional legal judgments or every task type.
- Agent outputs and controller observations were retained privately. Complete nested native tool transcripts were not available; no vendor-signed execution record is claimed. This public aggregate is author-reported and cannot replace independent reruns.
- The original source material and private audit records are not distributed. Only synthetic fixtures, rubrics and this aggregate are public.
- Structural validation and installation checks demonstrate packaging properties, not semantic reliability. Use the Skill's independent review and evidence rules in each real task.

See [results.json](results.json) for the final closure and transfer counts, and [README](README.md) for rerun instructions.
