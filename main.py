import argparse
import os
import sys

from core.case_manager import create_case, add_evidence_to_case
from core.report_generator import (
    generate_executive_summary,
    generate_technical_report,
    generate_chain_of_custody,
    generate_full_case_export
)


# -------------------------------------------------------------
# Main CLI Function
# -------------------------------------------------------------
def main():
    """
    Entry point for MetaTrace forensic toolkit.
    Handles:
    - Case creation/loading
    - Evidence processing
    - Report generation
    """

    parser = argparse.ArgumentParser(
        description="MetaTrace Digital Forensics Toolkit"
    )

    parser.add_argument(
        "case",
        help="Name of the forensic case"
    )

    parser.add_argument(
        "filepath",
        help="Path to evidence file"
    )

    args = parser.parse_args()

    case_name = args.case
    file_path = args.filepath

    # ---------------------------------------------------------
    # Validate Evidence File Exists
    # ---------------------------------------------------------
    if not os.path.exists(file_path):
        print("Error: Evidence file not found.")
        sys.exit(1)

    case_path = os.path.join("cases", case_name)

    # ---------------------------------------------------------
    # Create or Load Case
    # ---------------------------------------------------------
    if not os.path.exists(case_path):
        print(f"Creating new case: {case_name}")
        create_case(case_name)
    else:
        print(f"Loading existing case: {case_name}")

    print("Adding evidence to case...")

    # ---------------------------------------------------------
    # Add Evidence
    # ---------------------------------------------------------
    result = add_evidence_to_case(case_name, file_path)

    if result is None:
        print("Evidence was not added (duplicate detected).")
        sys.exit(0)

    print("Evidence successfully processed.")

    # ---------------------------------------------------------
    # Generate Reports
    # ---------------------------------------------------------
    print("Generating reports...")

    generate_executive_summary(case_name)
    generate_technical_report(case_name)
    generate_chain_of_custody(case_name)
    generate_full_case_export(case_name)

    print("Reports generated successfully.")
    print("Check case folder for recovered artefacts and reports.")


# -------------------------------------------------------------
# Run Program
# -------------------------------------------------------------
if __name__ == "__main__":
    main()
