import os  # Used to create directories and manage file paths
from datetime import datetime  # Used for timestamping analysis reports


def save_analysis_report(metadata, file_hash):
    """
    Saves structured forensic analysis results to a timestamped report file.
    Returns the path of the generated report.
    """

    # --- Ensure Output Directory Exists ---
    os.makedirs("output", exist_ok=True)

    # --- Generate Timestamped Filename ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"output/analysis_{timestamp}.txt"

    # --- Write Structured Forensic Report ---
    with open(report_filename, "w") as report:

        report.write("MetaTrace Forensic Analysis Report\n")
        report.write("----------------------------------\n\n")

        report.write(f"Analysis Timestamp: {datetime.now()}\n\n")

        report.write(f"Target File: {metadata['absolute_path']}\n")
        report.write(f"File Size (bytes): {metadata['file_size_bytes']}\n")
        report.write(f"Created Time: {metadata['created_time']}\n")
        report.write(f"Modified Time: {metadata['modified_time']}\n")
        report.write(f"Last Accessed Time: {metadata['accessed_time']}\n")
        report.write(f"SHA-256 Hash: {file_hash}\n")

    # --- Return Report Path For CLI Output ---
    return report_filename
