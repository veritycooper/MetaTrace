# --- Global Case Context ---
current_case_path = None


# --- Set Active Case ---
def set_current_case(path):
    global current_case_path
    current_case_path = path


# --- Get Active Case ---
def get_current_case():
    return current_case_path
