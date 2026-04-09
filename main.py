import argparse  # Library used to handle command-line arguments
import os        # Used to check if the file exists
import sys       # Used for controlled program exit


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
        print("Error: The specified file does not exist.")
        sys.exit(1)

    # Display structured runtime information
    print("MetaTrace Runtime Information")
    print("------------------------------")
    print(f"Target File: {args.filepath}")


# Standard Python entry point check
if __name__ == "__main__":
    main()
