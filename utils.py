import re


def remove_brackets(s):
    parts = re.split('\[|\]', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('\(|\)', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('<|>', s)
    return ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])


def num_to_superscript(num):
    return ''.join([{'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                     '+': '⁺', '-': '⁻', '.': '⋅'}[d] for d in str(num)])
