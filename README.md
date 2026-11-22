# Synthetic Clinical Study Metrics

Educational, privacy-safe examples for clinical data reporting. All records in this repository are fictitious.

## Quick start

```bash
python examples/synthetic_trial_metrics.py
```

The Python example groups study participants by site and recruitment status using standard-library dataclasses. It does not perform clinical research calculations or use production patient information.

Recommended additions: input schema validation, anonymized test fixtures, unit tests, and study-level aggregation reports. Never commit actual patient records or regulated healthcare data.
