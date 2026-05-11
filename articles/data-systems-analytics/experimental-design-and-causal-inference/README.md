# Experimental Design and Causal Inference

This companion code models causal inference as evidence infrastructure: causal questions, interventions, estimands, treatment assignment, randomization checks, blocking, factorial structure, quasi-experimental designs, difference-in-differences, regression discontinuity, propensity weighting, validity review, and causal governance.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Causal inference asks what would change under intervention.

```text
causal question → intervention → estimand → design / identification
        → estimation → robustness checks → validity review
        → causal claim with stated assumptions
```

A mature causal workflow does not ask only whether variables are associated. It asks whether the comparison is credible enough to stand in for the missing counterfactual.
