import os
import json
from datetime import datetime


# -------------------------------------------------------------
# Helper: Load Case Data
# -------------------------------------------------------------
def load_case_data(case_name):
    case_path = os.path.join("cases", case_name)

    timeline_path = os.path.join(case_path, "timeline.json")
    metadata_path = os.path.join(case_path, "case_metadata.json")

    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return case_path, timeline, metadata


# -------------------------------------------------------------
# Executive Summary Report
# -------------------------------------------------------------
def generate_executive_summary(case_name):
    case_path, timeline, metadata = load_case_data(case_name)

    report_path = os.path.join(case_path, "reports", "Executive_Summary.txt")

    with open(report_path, "w") as f:
        f.write("=== EXECUTIVE SUMMARY ===\n")
        f.write(f"Case Name: {metadata['case_name']}\n")
        f.write(f"Date Generated: {datetime.now().isoformat()}\n\n")

        f.write(f"Total Evidence Items: {metadata['evidence_count']}\n\n")

        for entry in timeline:
            f.write(f"- Evidence ID: {entry['evidence_id']}\n")
            f.write(f"  File: {entry['file_name']}\n")
            f.write(f"  Hash Verified: {entry.get('hash_verified', False)}\n")
            f.write(f"  Malware Result: {entry['malware_scan_result']}\n")

            if entry.get("memory_analysis"):
                f.write(f"  Entropy Score: {entry['memory_analysis']['entropy_score']}\n")
                f.write(f"  Entropy Classification: {entry['memory_analysis']['entropy_classification']}\n")

            f.write("\n")

    print("Executive Summary generated.")
    return report_path


# -------------------------------------------------------------
# Technical Report
# -------------------------------------------------------------
def generate_technical_report(case_name):
    case_path, timeline, metadata = load_case_data(case_name)

    report_path = os.path.join(case_path, "reports", "Technical_Report.txt")

    with open(report_path, "w") as f:
        f.write("=== TECHNICAL FORENSIC REPORT ===\n")
        f.write(f"Case: {metadata['case_name']}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        for entry in timeline:
            f.write(f"Evidence ID: {entry['evidence_id']}\n")
            f.write(f"File Name: {entry['file_name']}\n")
            f.write(f"SHA-256: {entry['sha256_hash']}\n")
            f.write(f"Malware Result: {entry['malware_scan_result']}\n")
            f.write(f"Recovered Files: {len(entry['recovered_files'])}\n")

            if entry.get("memory_analysis"):
                f.write("Memory Analysis:\n")
                f.write(f"  Entropy Score: {entry['memory_analysis']['entropy_score']}\n")
                f.write(f"  Classification: {entry['memory_analysis']['entropy_classification']}\n")
                f.write(f"  Processes: {entry['memory_analysis']['detected_processes']}\n")
                f.write(f"  IP Addresses: {entry['memory_analysis']['detected_ip_addresses']}\n")

            f.write("\n----------------------------------------\n\n")

    print("Technical Report generated.")
    return report_path


# -------------------------------------------------------------
# Chain of Custody Report
# -------------------------------------------------------------
def generate_chain_of_custody(case_name):
    case_path, timeline, metadata = load_case_data(case_name)

    report_path = os.path.join(case_path, "reports", "Chain_of_Custody.txt")

    with open(report_path, "w") as f:
        f.write("=== CHAIN OF CUSTODY REPORT ===\n")
        f.write(f"Case: {metadata['case_name']}\n\n")

        for entry in timeline:
            f.write(f"Evidence ID: {entry['evidence_id']}\n")
            f.write(f"File: {entry['file_name']}\n")
            f.write(f"SHA-256: {entry['sha256_hash']}\n")
            f.write(f"Added: {entry['timestamp']}\n")
            f.write(f"Integrity Verified: {entry.get('hash_verified', False)}\n")
            f.write("\n")

    print("Chain of Custody report generated.")
    return report_path


# -------------------------------------------------------------
# FULL CASE EXPORT (All-in-One Upload File)
# -------------------------------------------------------------
def generate_full_case_export(case_name):
    case_path, timeline, metadata = load_case_data(case_name)

    report_path = os.path.join(case_path, "reports", "Full_Case_Export.txt")

    with open(report_path, "w") as f:
        f.write("=== FULL CASE EXPORT ===\n\n")
        f.write(f"Case Name: {metadata['case_name']}\n")
        f.write(f"Created: {metadata['created_at']}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        f.write("==== EVIDENCE SUMMARY ====\n\n")

        for entry in timeline:
            f.write(json.dumps(entry, indent=4))
            f.write("\n\n")

    print("Full Case Export generated.")
    return report_path
