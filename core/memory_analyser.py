import re
import math


# -------------------------------------------------------------
# Shannon Entropy Calculation
# -------------------------------------------------------------
def calculate_entropy(data):
    """
    Calculates Shannon entropy of binary data.
    High entropy may indicate encryption or packing.
    """

    if not data:
        return 0

    byte_frequency = [0] * 256

    for byte in data:
        byte_frequency[byte] += 1

    entropy = 0

    for freq in byte_frequency:
        if freq > 0:
            probability = freq / len(data)
            entropy -= probability * math.log2(probability)

    return entropy


# -------------------------------------------------------------
# Process Extraction (Volatility-Inspired Simulation)
# -------------------------------------------------------------
def extract_processes_from_memory(data):
    """
    Simple keyword scan for common Windows process names.
    """

    known_processes = [
        b"cmd.exe",
        b"powershell.exe",
        b"explorer.exe",
        b"svchost.exe",
        b"winlogon.exe"
    ]

    detected = []

    for process in known_processes:
        if process in data:
            detected.append(process.decode())

    return detected


# -------------------------------------------------------------
# IP Extraction
# -------------------------------------------------------------
def extract_ip_addresses(data):
    """
    Extract possible IPv4 addresses from memory dump.
    """

    text_data = data.decode(errors="ignore")
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

    return re.findall(ip_pattern, text_data)


# -------------------------------------------------------------
# Main Memory Analysis Function
# -------------------------------------------------------------
def analyse_memory_dump(file_path):
    """
    Performs:
    - Entropy analysis
    - Process detection
    - IP extraction
    """

    with open(file_path, "rb") as f:
        data = f.read()

    entropy_score = calculate_entropy(data)
    processes = extract_processes_from_memory(data)
    ip_addresses = extract_ip_addresses(data)

    print(f"Entropy Score: {entropy_score:.4f}")

    if entropy_score > 7.5:
        classification = "High"
        print("Entropy Classification: High (Possible encryption or obfuscation)")
    elif entropy_score > 6:
        classification = "Medium"
        print("Entropy Classification: Medium")
    else:
        classification = "Low"
        print("Entropy Classification: Low")

    return {
        "entropy_score": round(entropy_score, 4),
        "entropy_classification": classification,
        "detected_processes": processes,
        "detected_ip_addresses": ip_addresses
    }
