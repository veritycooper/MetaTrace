import os
from datetime import datetime

def extract_metadata(filepath):
    """
    Extracts key forensic metadata from a file.

    Returns:
        dict: structured metadata information
    """

    stats = os.stat(filepath)

    metadata = {
        "absolute_path": os.path.abspath(filepath),
        "file_size_bytes": stats.st_size,
        "created_time": datetime.fromtimestamp(stats.st_ctime),
        "modified_time": datetime.fromtimestamp(stats.st_mtime),
        "accessed_time": datetime.fromtimestamp(stats.st_atime),
    }

    return metadata
