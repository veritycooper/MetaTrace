import hashlib  # Provides secure hashing algorithms


def compute_sha256(filepath):
    """
    Computes the SHA-256 hash of a file.

    The file is read in chunks to support large file processing
    without loading the entire file into memory.
    """

    sha256 = hashlib.sha256()

    # Open file in binary mode
    with open(filepath, "rb") as file:
        # Read file in fixed-size chunks (4KB)
        while chunk := file.read(4096):
            sha256.update(chunk)

    # Return hexadecimal digest of the hash
    return sha256.hexdigest()
