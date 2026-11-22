"""CLI: validate synthetic enrollment CSV, write summary JSON.

python clinical/report.py examples/synthetic_enrollment.csv --output report.json
"""
import argparse
import json
from pathlib import Path
from quality import read_enrollments, site_summary, monthly_consents


def create_report(csv_path: Path) -> dict:
    enrollments = read_enrollments(csv_path)
    return {
        "source": csv_path.name,
        "subject_count": len(enrollments),
        "site_metrics": site_summary(enrollments),
        "monthly_consents": monthly_consents(enrollments),
        "disclaimer": "Synthetic educational example; not a validated clinical report",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path, help="Write JSON to this path")
    args = parser.parse_args()
    try:
        content = json.dumps(create_report(args.csv_file), indent=2)
        if args.output:
            args.output.write_text(content + "\n", encoding="utf-8")
            print(f"Wrote {args.output}")
        else:
            print(content)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
