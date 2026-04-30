import argparse  # Library used to handle command-line arguments
import os        # Used to check if the file exists
import sys       # Used for controlled program exit

from core.hashing import compute_sha256          # SHA-256 hashing function
from core.metadata import extract_metadata      # Metadata extraction function
from core.logger import save_analysis_report    # Text report generator
from core.json_export import save_json_report   # JSON structured report generator


def main():

    # --- CLI Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description="MetaTrace - Digital Forensics Hashing and Metadata Tool"
    )

    # --- Required Positional Argument (Target File Path) ---
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file to analyse"
    )

    # --- Optional Hash Verification Argument ---
    parser.add_argument(
        "--verify",
        type=str,
        help="Provide a known SHA-256 hash to verify file integrity"
    )

    # --- Parse User Arguments ---
    args = parser.parse_args()

    # --- Validate File Exists Before Continuing ---
    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' was not found.")
        sys.exit(1)

    # --- Compute SHA-256 Hash ---
    file_hash = compute_sha256(args.filepath)

    # --- Extract File Metadata ---
    file_metadata = extract_metadata(args.filepath)

    # --- Generate Structured Text Report (.txt) ---
    report_path = save_analysis_report(file_metadata, file_hash)

    # --- Generate Structured JSON Report (.json) ---
    json_path = save_json_report(file_metadata, file_hash)

    # --- Display Runtime Information ---
    print("\nMetaTrace Runtime Information")
    print("--------------------------------")

    print(f"Target File: {file_metadata['absolute_path']}")
    print(f"File Size (bytes): {file_metadata['file_size_bytes']}")
    print(f"Created Time: {file_metadata['created_time']}")
    print(f"Modified Time: {file_metadata['modified_time']}")
    print(f"Last Accessed Time: {file_metadata['accessed_time']}")
    print(f"SHA-256 Hash: {file_hash}")

    print(f"\nText report saved to: {report_path}")
    print(f"JSON report saved to: {json_path}")

    # --- Optional Hash Verification Logic ---
    if args.verify:

        print("\nHash Verification Result")
        print("------------------------")

        # Compare lowercase to avoid case sensitivity issues
        if file_hash.lower() == args.verify.lower():
            print("Status: MATCH ✅ File integrity verified.")
        else:
            print("Status: MISMATCH ❌ File may have been altered.")


# --- Standard Python Entry Point Check ---
if __name__ == "__main__":
    main()
