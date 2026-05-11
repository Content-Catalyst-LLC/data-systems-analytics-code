# Statistical Modeling and Inference

This companion code models statistical inference as evidence infrastructure: samples, estimands, standard errors, confidence intervals, hypothesis tests, regression coefficients, residual diagnostics, robustness flags, uncertainty records, and model-governance summaries.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Statistical inference turns finite data into qualified claims.

```text
sample data → model / estimand → estimate + uncertainty
        → diagnostics + assumptions → interpretation
        → evidence claim with limits
```

A mature inference workflow does not ask only whether a model returned a significant result. It asks whether the estimand is clear, assumptions are plausible, uncertainty is visible, diagnostics are reviewed, and substantive interpretation is proportionate.
