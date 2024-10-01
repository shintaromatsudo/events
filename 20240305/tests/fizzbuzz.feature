# fizzbuzz.feature

Feature: FizzBuzz

  Scenario: Fizzbuzz for multiples of 3 and 5
    Given I have a number 15
    When I check the number
    Then I should see fizzbuzz
