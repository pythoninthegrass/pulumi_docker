def convert_to_bytes(value_str: str) -> int:
    """
    Convert a string value with 'm' or 'g' suffix to bytes.

    Args:
        value_str: A string value with 'm' (megabytes) or 'g' (gigabytes) suffix

    Returns:
        The equivalent value in bytes

    Usage:
        '512m' -> 512 MiB in bytes
        '2g' -> 2 GiB in bytes

    Raises:
        ValueError: If the input string doesn't end with 'm' or 'g'
    """
    if not isinstance(value_str, str):
        raise ValueError("Value must be a string with 'm' or 'g' suffix")

    value_str = value_str.lower().strip()
    match value_str[-1]:
        case 'm':
            value = int(value_str[:-1])
            return value * 1024 * 1024
        case 'g':
            value = int(value_str[:-1])
            return value * 1024 * 1024 * 1024
        case _:
            raise ValueError("Value must end with 'm' or 'g'")
