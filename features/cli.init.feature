Feature: init project
  In order to find duplicates
  As a cli user
  I want to init projects

  Scenario: Run `init` in uninitialized project
    Given an uninitialized directory
    When  I run findd with ['init']
    Then  the exit_code is zero

  Scenario: Run `init` in initialized project
    Given an initialized directory
    When  I run findd with ['init']
    Then  the exit_code is non-zero
