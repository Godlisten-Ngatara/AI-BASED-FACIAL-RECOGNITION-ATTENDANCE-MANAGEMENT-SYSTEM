def split_name(full_name: str):
    parts = full_name.strip().split()

    if len(parts) == 1:
        return parts[0] # first=none, middle=none, last
    elif len(parts) == 2:
        return parts[0], None, parts[1]  # first, middle=None, last
    elif len(parts) == 3:
        return parts[0], parts[1], parts[2]  # first, middle, last
    else:
        raise ValueError("Invalid instructor name format. Use 'First Last' or 'First Middle Last'.")
