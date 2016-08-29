"""Utility functions"""


def mangle(path):
    """mangle the original file path to replace separators with underscores
    and double up existing underscores
    """
    mangled_path = ''
    for char in path:
        if char == '/':
            mangled_path += '_'
        elif char == '_':
            mangled_path += '__'
        else:
            mangled_path += char
    return mangled_path
