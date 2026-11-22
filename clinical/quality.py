"""Synthetic clinical trial enrollment validation and reporting utilities.

For demonstrations only; not a validated GxP or regulatory reporting system.
"""
from collections import Counter
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


VALID_STATUSES = {"screened", "screen_failed", "enrolled", "withdrawn", "completed"}


@dataclass(frozen=True)
class Enrollment:
    subject_id: str
    site_id: str
    status: str
    consent_date: date

    def __post_init__(self):
        if not self.subject_id.strip() or not self.site_id.strip():
            raise ValueError("Subject ID and site ID are required")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {self.status}")


def read_enrollments(path: Path) -> list[Enrollment]:
    """Read synthetic CSV rows, failing fast on invalid or duplicate identifiers."""
    results = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"subject_id", "site_id", "status", "consent_date"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Missing headers: {sorted(required - set(reader.fieldnames or []))}")
        for line, row in enumerate(reader, 2):
            try:
                subject = Enrollment(
                    row["subject_id"].strip(),
                    row["site_id"].strip(),
                    row["status"].strip().lower(),
                    date.fromisoformat(row["consent_date"].strip()),
                )
            except (AttributeError, TypeError, ValueError) as error:
                raise ValueError(f"Line {line}: {error}") from error
            if subject.subject_id in seen:
                raise ValueError(f"Line {line}: Duplicate subject ID {subject.subject_id}")
            seen.add(subject.subject_id)
            results.append(subject)
    return results


def site_summary(enrollments: list[Enrollment]) -> list[dict[str, int | str | float]]:
    sites: dict[str, Counter[str]] = {}
    for row in enrollments:
        sites.setdefault(row.site_id, Counter())[row.status] += 1
    result = []
    for site_id, statuses in sorted(sites.items()):
        total = sum(statuses.values())
        result.append({
            "site_id": site_id,
            "subjects": total,
            "screened": statuses["screened"],
            "screen_failed": statuses["screen_failed"],
            "enrolled": statuses["enrolled"],
            "withdrawn": statuses["withdrawn"],
            "completed": statuses["completed"],
            "enrollment_fraction": round(
                (statuses["enrolled"] + statuses["completed"] + statuses["withdrawn"]) / total, 4
            ) if total else 0.0,
        })
    return result


def monthly_consents(enrollments: list[Enrollment]) -> list[dict[str, str | int]]:
    counts = Counter(row.consent_date.strftime("%Y-%m") for row in enrollments)
    return [{"month": month, "consents": counts[month]} for month in sorted(counts)]
