import argparse  # Library used to handle command-line arguments
import os        # Used to check if the file exists
import sys       # Used for controlled program exit
from core.hashing import compute_sha256 # Used for hashing
from core.metadata import extract_metadata # Used for extracting metadata

def main():
    # Create the command-line argument parser
    parser = argparse.ArgumentParser(
        description="MetaTrace - Digital Forensics Hashing and Metadata Tool"
    )
    
    # Define required positional argument for the target file path
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file to analyse"
    )

    # Parse user-provided arguments
    args = parser.parse_args()

    # Validate that the file exists before continuing
    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' was not found.") # updated commit in phase 2 
        sys.exit(1)

    # Compute SHA-256 hash of the validated file
    file_hash = compute_sha256(args.filepath)
    file_metadata = extract_metadata(args.filepath)

    # Display structured runtime information
    print("MetaTrace Runtime Information")
    print("--------------------------------")

    print(f"Target File: {file_metadata['absolute_path']}")
    print(f"File Size (bytes): {file_metadata['file_size_bytes']}")
    print(f"Created Time: {file_metadata['created_time']}")
    print(f"Modified Time: {file_metadata['modified_time']}")
    print(f"Last Accessed Time: {file_metadata['accessed_time']}")
    print(f"SHA-256 Hash: {file_hash}")


# Standard Python entry point check
if __name__ == "__main__":
    main()
