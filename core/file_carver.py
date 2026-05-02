import os

# -------------------------------------------------------------
# Function: carve_deleted_files
# Purpose:
#   Scan raw file data using header + footer detection
#   for more precise carving.
# -------------------------------------------------------------
def carve_deleted_files(file_path, output_folder):

    # --- File signatures with headers and footers ---
    signatures = {
        "jpg": {
            "header": b"\xFF\xD8\xFF",
            "footer": b"\xFF\xD9"
        },
        "png": {
            "header": b"\x89PNG\r\n\x1a\n",
            "footer": b"IEND\xAE\x42\x60\x82"
        },
        "pdf": {
            "header": b"%PDF",
            "footer": b"%%EOF"
        }
    }

    recovered_files = []
    os.makedirs(output_folder, exist_ok=True)

    with open(file_path, "rb") as f:
        data = f.read()

    for file_type, sig in signatures.items():

        header = sig["header"]
        footer = sig["footer"]
        start = 0

        while True:
            header_offset = data.find(header, start)

            if header_offset == -1:
                break

            footer_offset = data.find(footer, header_offset)

            if footer_offset == -1:
                break

            end_offset = footer_offset + len(footer)

            carved_data = data[header_offset:end_offset]

            recovered_filename = f"recovered_{len(recovered_files)+1}.{file_type}"
            recovered_path = os.path.join(output_folder, recovered_filename)

            with open(recovered_path, "wb") as out_file:
                out_file.write(carved_data)

            recovered_files.append(recovered_filename)

            start = end_offset

    return recovered_files
