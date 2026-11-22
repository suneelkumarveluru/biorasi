"""Demonstrate clinical study metrics using synthetic data only.

No real patient or study data is included.
"""
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Subject:
    subject_id: str
    site: str
    status: str


def summarize(subjects: list[Subject]) -> dict[str, dict[str, int]]:
    by_site: dict[str, Counter[str]] = {}
    for subject in subjects:
        by_site.setdefault(subject.site, Counter())[subject.status] += 1
    return {site: dict(counts) for site, counts in sorted(by_site.items())}


if __name__ == "__main__":
    subjects = [
        Subject("DEMO-001", "SITE-A", "screened"),
        Subject("DEMO-002", "SITE-A", "enrolled"),
        Subject("DEMO-003", "SITE-B", "enrolled"),
    ]
    print(summarize(subjects))
