# from hypothesis import given, note, strategies as st
# from src.fizzbuzz import fizz_buzz


# def test_fizz():
#     assert fizz_buzz(3) == "fizz"


# def test_buzz():
#     assert fizz_buzz(5) == "buzz"


# @given(st.integers(min_value=1))
# def test_fizzbuzz(n):
#     note(f"n: {n}")
#     if n % 3 == 0 and n % 5 == 0:
#         assert fizz_buzz(n) == "fizzbuzz"
#     elif n % 3 == 0:
#         assert fizz_buzz(n) == "fizz"
#     elif n % 5 == 0:
#         assert fizz_buzz(n) == "buzz"
#     else:
#         assert fizz_buzz(n) == n
