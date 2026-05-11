# Provenance model

A minimal reproducible analytics manifest should answer six questions.

1. **What input state was used?**
   - source path
   - snapshot path
   - row count
   - cryptographic or content fingerprint

2. **What code state was used?**
   - repository
   - commit hash when available
   - workflow version
   - script path

3. **What environment executed the workflow?**
   - language runtime
   - operating system
   - dependency files
   - container image or lockfile where applicable

4. **What parameters shaped the run?**
   - time window
   - filters
   - grouping choices
   - thresholds
   - output format choices

5. **What artifacts were produced?**
   - output file paths
   - output fingerprints
   - generated metadata
   - log files

6. **How can the run be repeated or compared?**
   - run id
   - timestamp
   - command
   - input snapshot
   - versioned code state
