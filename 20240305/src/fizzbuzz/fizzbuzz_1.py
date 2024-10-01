# fizzbuz_1.py
def fizz_buzz(n):
    if n % 15 == 0:
        return "fizzbuzz"

    if n % 3 == 0:
        return "fizz"

    if n % 5 == 0:
        return "buzz"

    return n
