import math

# -------------------------------------------------------------
# Function: calculate_shannon_entropy
# Purpose:
#   Calculates Shannon entropy of a file.
#   Used to detect encryption, packing, obfuscation.
# -------------------------------------------------------------
def calculate_shannon_entropy(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    if not data:
        return 0.0

    byte_counts = [0] * 256

    for byte in data:
        byte_counts[byte] += 1

    entropy = 0.0
    data_length = len(data)

    for count in byte_counts:
        if count == 0:
            continue
        probability = count / data_length
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


# -------------------------------------------------------------
# Function: classify_entropy
# Purpose:
#   Provides human-readable classification of entropy score
# -------------------------------------------------------------
def classify_entropy(entropy_score):

    if entropy_score < 4.0:
        return "Low (Likely plain text or structured data)"

    elif 4.0 <= entropy_score < 7.0:
        return "Moderate (Compressed or mixed content)"

    else:
        return "High (Possible encryption, packing, or obfuscation)"
