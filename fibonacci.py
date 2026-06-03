"""
Fibonacci number calculator with test cases.

This module provides a function to compute the nth Fibonacci number
using an iterative approach for efficiency.
"""


def fibonacci(n: int) -> int:
    """
    Return the nth Fibonacci number.

    The Fibonacci sequence is defined as:
        F(0) = 0
        F(1) = 1
        F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: The index in the Fibonacci sequence (non-negative integer).

    Returns:
        The nth Fibonacci number.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
    """
    if not isinstance(n, int):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be a non-negative integer, got {n}")

    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def main():
    """Run test cases for the fibonacci function."""
    test_cases = [
        # (input, expected_output)
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (20, 6765),
        (30, 832040),
    ]

    print("Running Fibonacci test cases...")
    all_passed = True

    for n, expected in test_cases:
        result = fibonacci(n)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  fibonacci({n}) = {result} (expected {expected}) [{status}]")

    # Test error handling
    error_cases = [
        # (input, expected_exception)
        (-1, ValueError),
        (3.5, TypeError),
        ("10", TypeError),
    ]

    print("\nRunning error handling test cases...")
    for n, expected_exception in error_cases:
        try:
            fibonacci(n)
            print(f"  fibonacci({n!r}) -> no exception raised [FAIL]")
            all_passed = False
        except expected_exception:
            print(f"  fibonacci({n!r}) -> {expected_exception.__name__} [PASS]")
        except Exception as e:
            print(f"  fibonacci({n!r}) -> unexpected {type(e).__name__}: {e} [FAIL]")
            all_passed = False

    print()
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")

    return all_passed


if __name__ == "__main__":
    main()
