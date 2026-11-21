import re

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def lines(a, b):
    """Return lines in both a and b"""
    return list(set(a.splitlines()) & set(b.splitlines()))


def sentences(a, b):
    """Return sentences in both a and b"""

    def split(text):
        return {s.strip() for s in _SENTENCE_END.split(text) if s.strip()}

    return list(split(a) & split(b))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    if n <= 0:
        return []

    def subs(text):
        return {text[i:i + n] for i in range(len(text) - n + 1)}

    return list(subs(a) & subs(b))
