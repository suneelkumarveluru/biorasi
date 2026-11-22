# Synthetic study enrollment reporting

A local, dependency-free CSV validation and reporting program using Python 3.10+.

## Usage

```bash
python clinical/report.py examples/synthetic_enrollment.csv
python clinical/report.py examples/synthetic_enrollment.csv --output report.json
python -m unittest discover -s tests -v
```

The tool requires `subject_id,site_id,status,consent_date`. Dates use ISO `YYYY-MM-DD`. Subjects must have unique IDs and one current status. Accepted statuses: `screened`, `screen_failed`, `enrolled`, `withdrawn`, `completed`.

Outputs per-site counts, current-status fractions, and consent counts by calendar month.

## Important assumptions

- **Synthetic records only.** This project is not a regulated/validated system and contains no patient data.
- Each subject has one latest status, not a longitudinal event history.
- `enrollment_fraction` is an illustrative proportion of statuses (enrolled, completed, withdrawn) rather than a clinical KPI definition.
- Consent date represents a recorded demo date; no protocol-level review is performed.
- Production clinical systems require governance, traceability, audit trails, validation evidence, study-specific protocol definitions and access controls.
