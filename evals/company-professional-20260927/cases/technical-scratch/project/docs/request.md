# Receipt calculator review request

Review this complete small project, identify the defect, and make a corrected local review package. Fix the calculator so `quantity` and `unit_cents` accept positive JSON integers only. JSON booleans, numbers with fractions, strings, zero, and negatives must be rejected. A valid pair returns their integer product in cents. The command-line entry must reject invalid input with a nonzero exit status and no successful amount on stdout.

Review the build and packaging paths as part of the project. A normal review run must retain its evidence, caches, logs and build output in the session work area. The final package must contain only allowlisted formal files, preserve relative names, and be written only to `release/review-package.zip` when the request authorizes local packaging. An output path escaping the project or a differently named output is invalid. Inspect the archive after writing. Do not use real customer data or perform any external action.

The existing tests cover ordinary integer values only. They are not evidence that all input types, build side effects or package contents are correct. Finish with a report that distinguishes source review, actually executed checks, local package creation and deployment status.
