import os      # Used to create directories and manage file paths
import json    # Used to generate structured JSON output
from datetime import datetime  # Used to timestamp analysis sessions


def save_json_report(metadata, file_hash):
    """
    Generates a structured JSON forensic report.

    Args:
        metadata (dict): Extracted file metadata
        file_hash (str): Computed SHA-256 hash

    Returns:
        str: Path to the generated JSON report
    """

    # --- Ensure Output Directory Exists ---
    os.makedirs("output", exist_ok=True)

    # --- Generate Timestamped Filename ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"output/analysis_{timestamp}.json"

    # --- Convert Datetime Objects To Strings ---
    # JSON cannot serialize datetime objects directly
    serializable_metadata = {
        "absolute_path": metadata["absolute_path"],
        "file_size_bytes": metadata["file_size_bytes"],
        "created_time": str(metadata["created_time"]),
        "modified_time": str(metadata["modified_time"]),
        "accessed_time": str(metadata["accessed_time"])
    }

    # --- Build Structured Forensic Data Object ---
    structured_data = {
        "analysis_timestamp": str(datetime.now()),
        "target_file": metadata["absolute_path"],
        "sha256_hash": file_hash,
        "metadata": serializable_metadata
    }

    # --- Write JSON Report To File ---
    with open(json_filename, "w") as json_file:
        json.dump(structured_data, json_file, indent=4)

    # --- Return JSON File Path For CLI Display ---
    return json_filename
