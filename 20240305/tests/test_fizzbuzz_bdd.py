# test_fizzbuzz.py

from pytest_bdd import scenario, given, when, then
from src.fizzbuzz.fizzbuzz_1 import fizz_buzz


@scenario("fizzbuzz.feature", "Fizzbuzz for multiples of 3 and 5")
def test_fizzbuzz():
    pass


@given("I have a number 15", target_fixture="number")
def number():
    return 15


@when("I check the number", target_fixture="check_number")
def check_number(number):
    return fizz_buzz(number)


@then("I should see fizzbuzz")
def fizzbuzz_result(check_number):
    assert check_number == "fizzbuzz"
