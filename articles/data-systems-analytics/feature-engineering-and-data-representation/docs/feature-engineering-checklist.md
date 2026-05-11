# Feature engineering checklist

- [ ] The raw-to-feature transformation is documented.
- [ ] Numerical variables are scaled or transformed when model family requires it.
- [ ] Categorical variables are encoded without false ordinal assumptions.
- [ ] High-cardinality categories have OOV, hashing, or embedding strategy.
- [ ] Feature crosses are justified by interaction logic.
- [ ] Temporal features represent cycles and cutoff time correctly.
- [ ] Derived variables reflect domain knowledge and not post-outcome leakage.
- [ ] Feature selection is performed inside validation workflow.
- [ ] Feature lineage connects source fields to model inputs.
- [ ] Representation metrics track dimensionality, sparsity, and approval status.
