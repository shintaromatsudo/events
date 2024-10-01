def fizz_buzz(n):
    if n % 3 == 0:
        if n % 5 == 0:
            return "fizzbuzz"
        else:
            return "fizz"
    if n % 5 == 0:
        if n % 3 == 0:
            return "fizzbuzz"
        else:
            return "buzz"
    return n
