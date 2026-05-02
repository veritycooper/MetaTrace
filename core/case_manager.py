import os
import shutil
import json
from datetime import datetime

from core.hashing import compute_sha256
from core.metadata import extract_metadata
from core.malware_scanner import scan_file_for_malware
from core.file_carver import carve_deleted_files
from core.memory_analyser import analyse_memory_dump
from core.entropy_analyser import calculate_shannon_entropy, classify_entropy

# -------------------------------------------------------------
# Function: create_case
# Purpose: Create structured forensic case directory
# -------------------------------------------------------------
def create_case(case_name):

    case_path = os.path.join("cases", case_name)

    # --- Create main case folder ---
    os.makedirs(case_path, exist_ok=True)

    # --- Create required subdirectories ---
    os.makedirs(os.path.join(case_path, "evidence"), exist_ok=True)
    os.makedirs(os.path.join(case_path, "reports"), exist_ok=True)
    os.makedirs(os.path.join(case_path, "logs"), exist_ok=True)
    os.makedirs(os.path.join(case_path, "recovered"), exist_ok=True)

    # --- Create timeline file if missing ---
    timeline_path = os.path.join(case_path, "timeline.json")
    if not os.path.exists(timeline_path):
        with open(timeline_path, "w") as f:
            json.dump([], f, indent=4)

    # --- Create case metadata if missing ---
    metadata_path = os.path.join(case_path, "case_metadata.json")
    if not os.path.exists(metadata_path):
        case_metadata = {
            "case_name": case_name,
            "created_at": datetime.now().isoformat(),
            "evidence_count": 0,
            "last_activity": datetime.now().isoformat(),
            "status": "Active"
        }

        with open(metadata_path, "w") as f:
            json.dump(case_metadata, f, indent=4)

    return case_path


# -------------------------------------------------------------
# Function: add_evidence_to_case
# Purpose:
#   - Copy file into case
#   - Hash file
#   - Verify integrity
#   - Calculate entropy
#   - Scan for malware
#   - Detect disk image
#   - Detect memory dump
#   - Attempt carving
#   - Log structured timeline entry
# -------------------------------------------------------------
def add_evidence_to_case(case_name, file_path):

    case_path = os.path.join("cases", case_name)
    evidence_folder = os.path.join(case_path, "evidence")

    if not os.path.exists(case_path):
        raise Exception("Case does not exist.")

    filename = os.path.basename(file_path)
    destination = os.path.join(evidence_folder, filename)

    # -------------------------------------------------------------
    # Step 1: Copy File
    # -------------------------------------------------------------
    shutil.copy2(file_path, destination)

    # -------------------------------------------------------------
    # Step 2: Calculate Original Hash
    # -------------------------------------------------------------
    print("Calculating original hash...")
    original_hash = compute_sha256(file_path)

    print("Verifying copied file integrity...")
    copied_hash = compute_sha256(destination)

    hash_verified = original_hash == copied_hash

    if hash_verified:
        print("Hash verification successful. Integrity confirmed.")
    else:
        print("WARNING: Hash mismatch detected.")

    # -------------------------------------------------------------
    # Step 3: Calculate File Entropy (ALL files)
    # -------------------------------------------------------------
    entropy_score = calculate_shannon_entropy(destination)
    entropy_classification = classify_entropy(entropy_score)

    print(f"Entropy Score: {entropy_score}")
    print(f"Entropy Classification: {entropy_classification}")

    # -------------------------------------------------------------
    # Step 4: Malware Scan
    # -------------------------------------------------------------
    malware_result = scan_file_for_malware(destination)
    print(f"Malware Scan Result: {malware_result}")

    # -------------------------------------------------------------
    # Step 5: Disk Image Detection
    # -------------------------------------------------------------
    disk_image_extensions = (".dd", ".img", ".raw", ".bin")

    if file_path.lower().endswith(disk_image_extensions):
        print("Disk image detected. Performing raw forensic carving.")
        disk_image_detected = True
    else:
        disk_image_detected = False

    # -------------------------------------------------------------
    # Step 6: Memory Dump Detection
    # -------------------------------------------------------------
    memory_extensions = (".mem", ".dmp", ".dump")

    memory_results = {}
    if file_path.lower().endswith(memory_extensions):
        print("Memory dump detected. Performing memory analysis.")
        memory_dump_detected = True
        memory_results = analyse_memory_dump(destination)
    else:
        memory_dump_detected = False

    # -------------------------------------------------------------
    # Step 7: Attempt File Carving
    # -------------------------------------------------------------
    recovery_folder = os.path.join(case_path, "recovered")
    recovered_files = carve_deleted_files(destination, recovery_folder)

    # -------------------------------------------------------------
    # Step 8: Extract Metadata
    # -------------------------------------------------------------
    metadata = extract_metadata(destination)

    # -------------------------------------------------------------
    # Step 9: Load Existing Timeline
    # -------------------------------------------------------------
    timeline_path = os.path.join(case_path, "timeline.json")

    try:
        with open(timeline_path, "r") as f:
            timeline_data = json.load(f)
    except:
        timeline_data = []

    # -------------------------------------------------------------
    # Step 10: Duplicate Detection (SHA-256)
    # -------------------------------------------------------------
    for existing_entry in timeline_data:
        if existing_entry.get("sha256_hash") == copied_hash:
            print("Duplicate evidence detected. Evidence not added.")
            os.remove(destination)
            return None

    # -------------------------------------------------------------
    # Step 11: Generate Evidence ID
    # -------------------------------------------------------------
    evidence_id = f"EVID-{len(timeline_data)+1:04d}"

    # -------------------------------------------------------------
    # Step 12: Create Structured Timeline Entry
    # -------------------------------------------------------------
    entry = {
        "evidence_id": evidence_id,
        "event_type": "Evidence Added",
        "timestamp": datetime.now().isoformat(),
        "file_name": filename,
        "sha256_hash": copied_hash,
        "hash_verified": hash_verified,
        "entropy_score": entropy_score,
        "entropy_classification": entropy_classification,
        "malware_scan_result": malware_result,
        "disk_image_detected": disk_image_detected,
        "memory_dump_detected": memory_dump_detected,
        "memory_analysis": memory_results,
        "recovered_files": recovered_files,
        "metadata": metadata
    }

    timeline_data.append(entry)

    with open(timeline_path, "w") as f:
        json.dump(timeline_data, f, indent=4)

    # -------------------------------------------------------------
    # Step 13: Update Case Metadata
    # -------------------------------------------------------------
    metadata_path = os.path.join(case_path, "case_metadata.json")

    with open(metadata_path, "r") as f:
        case_metadata = json.load(f)

    case_metadata["evidence_count"] += 1
    case_metadata["last_activity"] = datetime.now().isoformat()

    with open(metadata_path, "w") as f:
        json.dump(case_metadata, f, indent=4)

    # -------------------------------------------------------------
    # Step 14: Activity Log
    # -------------------------------------------------------------
    log_path = os.path.join(case_path, "logs", "activity.log")

    with open(log_path, "a") as log_file:
        log_file.write(
            f"[{datetime.now().isoformat()}] "
            f"Evidence {evidence_id} added | "
            f"Hash Verified: {hash_verified} | "
            f"Entropy: {entropy_score} | "
            f"Malware: {malware_result}\n"
        )

    return entry
