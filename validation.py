def validate_in_range(value, begin_value = None, end_value = None) -> bool:
    gr_begin = begin_value <= value if begin_value else True
    ls_end = value <= end_value if end_value else True
    return gr_begin and ls_end


def all_in_range(values: list, begin_value = None, end_value = None) -> bool:
    return all(validate_in_range(value, begin_value, end_value) for value in values)


def validate_rgba_code(value) -> bool:
    if type(value) is not str:
        return False
    
    value: str = value.lower()
    if value[0] == "#":
        value = value[1:]
    
    if len(value) != 6:
        return False
    
    allowed_chars = [str(i) for i in range(10)] + ["a", "b", "c", "d", "e", "f"]
    return all((char in allowed_chars) for char in value)


def all_rgba_code(values: list) -> bool:
    return all(validate_rgba_code(value) for value in values)
