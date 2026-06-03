"""
pal.py

A small module providing two palindrome-checker implementations.

Both functions treat the input as **ASCII-only**: non-ASCII characters are
stripped before the palindrome test.  This makes the two implementations
behaviourally identical.
"""

from __future__ import annotations

import re


def _is_ascii_alnum(c: str) -> bool:
    """Return True if *c* is an ASCII alphanumeric character."""
    return c.isalnum() and ord(c) < 128


def is_palindrome(text: str) -> bool:
    """
    Return True if *text* is a palindrome, ignoring case, punctuation,
    whitespace, and non-ASCII characters.

    This implementation builds a cleaned string and compares it with its
    reverse.

    Parameters
    ----------
    text : str
        The string to test.

    Returns
    -------
    bool
        True when the ASCII-alphanumeric skeleton of *text* reads the same
        forwards and backwards.

    Raises
    ------
    TypeError
        If *text* is ``None``.

    Examples
    --------
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("")
    True
    """
    if text is None:
        raise TypeError("Input text cannot be None")

    # Strip everything that is not an ASCII letter or digit.
    cleaned = re.sub(r"[^A-Za-z0-9]", "", text).lower()
    return cleaned == cleaned[::-1]


def is_palindrome_manual(text: str) -> bool:
    """
    Return True if *text* is a palindrome, ignoring case, punctuation,
    whitespace, and non-ASCII characters.

    This implementation uses a two-pointer scan and works in O(1) extra
    space (not counting the input string itself).

    Parameters
    ----------
    text : str
        The string to test.

    Returns
    -------
    bool
        True when the ASCII-alphanumeric skeleton of *text* reads the same
        forwards and backwards.

    Raises
    ------
    TypeError
        If *text* is ``None``.

    Examples
    --------
    >>> is_palindrome_manual("Racecar")
    True
    >>> is_palindrome_manual("Python")
    False
    >>> is_palindrome_manual("a!!a")
    True
    """
    if text is None:
        raise TypeError("Input text cannot be None")

    left, right = 0, len(text) - 1

    while left < right:
        # Advance left pointer past ignored characters.
        while left < right and not _is_ascii_alnum(text[left]):
            left += 1
        # Retreat right pointer past ignored characters.
        while left < right and not _is_ascii_alnum(text[right]):
            right -= 1

        # If the pointers have crossed, we have examined every valid pair.
        if left >= right:
            return True

        # Compare the valid characters case-insensitively.
        if text[left].lower() != text[right].lower():
            return False

        left += 1
        right -= 1

    return True


if __name__ == "__main__":
    test_cases = [
        # (input, expected_result)
        ("", True),
        ("a", True),
        ("aa", True),
        ("ab", False),
        ("aba", True),
        ("abc", False),
        ("A man, a plan, a canal: Panama", True),
        ("No 'x' in Nixon", True),
        ("hello", False),
        ("!!!", True),          # pure punctuation -> empty -> True
        ("   ", True),          # pure whitespace -> empty -> True
        ("a!!a", True),         # punctuation between matching chars
        ("a!!b", False),
        ("上海自来水来自海上", True),   # Unicode stripped -> empty -> True
        ("上海", True),               # Unicode stripped -> empty -> True
        ("Madam, 我是人, 是人 amaD", False),  # ASCII remainder not palindrome
    ]

    all_passed = True
    for s, expected in test_cases:
        for func in (is_palindrome, is_palindrome_manual):
            result = func(s)
            if result != expected:
                print(
                    f"FAIL: {func.__name__}({s!r}) = {result}, expected {expected}"
                )
                all_passed = False

    # Verify TypeError is raised for None input.
    for func in (is_palindrome, is_palindrome_manual):
        try:
            func(None)  # type: ignore[arg-type]
            print(f"FAIL: {func.__name__}(None) did not raise TypeError")
            all_passed = False
        except TypeError:
            pass

    if all_passed:
        print("All tests passed.")
