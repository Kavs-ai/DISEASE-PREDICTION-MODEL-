def validate_input(disease, data):
    if not disease or not data:
        return False, "Missing disease or data"

    if not isinstance(data, dict):
        return False, "Invalid data format"

    if len(data) < 4:
        return False, "Not enough input features"

    for key, value in data.items():
        try:
            float(value)
        except:
            return False, f"Invalid value for {key}"

    return True, None