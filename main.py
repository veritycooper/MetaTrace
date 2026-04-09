import argparse  # Library used to handle command-line arguments


def main():
    # Create the command-line argument parser
    parser = argparse.ArgumentParser(
        description="MetaTrace - Digital Forensics Hashing and Metadata Tool"
    )

    # Define a required positional argument for the target file path
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file to analyse"
    )

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Display structured runtime information
    print("MetaTrace Runtime Information")
    print("------------------------------")
    print(f"Target File: {args.filepath}")


# Standard Python entry point check
# Ensures main() runs only when the script is executed directly
if __name__ == "__main__":
    main()
