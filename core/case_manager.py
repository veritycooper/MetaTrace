import os
import json
from datetime import datetime


# --- Create New Case Directory Structure ---
def create_case(case_name):
    """
    Creates a new case folder with required subdirectories.
    """

    # --- Define Base Case Path ---
    base_path = os.path.join("cases", case_name)

    # --- Create Folder Structure ---
    os.makedirs(os.path.join(base_path, "evidence"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "reports"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "logs"), exist_ok=True)

    # --- Create Case Metadata File ---
    case_metadata = {
        "case_name": case_name,
        "created_at": str(datetime.now()),
        "last_activity": str(datetime.now()),
        "status": "Active"
    }

    metadata_path = os.path.join(base_path, "case_metadata.json")

    with open(metadata_path, "w") as file:
        json.dump(case_metadata, file, indent=4)

    return base_path
