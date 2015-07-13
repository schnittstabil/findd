Feature: update project
  In order to find duplicates
  As a user
  I want to update a project

  Scenario: Run `update` in an uninitialized project
    Given an uninitialized directory
    When  I run findd with ['update']
    Then  the exit_code is non-zero

  Scenario: Run `update` in an initialized project
    Given an initialized directory
    When  I run findd with ['update']
    Then  the exit_code is zero

  Scenario: Run `update` after deleting files
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 000     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I delete the files ['dir/b']
    And  I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches '^$'

  Scenario: Run `update` after changing files of diffrent size
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 0       |
    When I run findd with ['update']
    And  I change content of file 'dir/a' to '123'
    And  I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^'a' 'dir[/\\]a'$"

  Scenario: Run `update` after changing files of same size
    Given an initialized directory
    And containing files:
      | path   | content | mtime_offset |
      | a      | 123     | -1           |
      | dir/a  | 000     | -1           |
    When I run findd with ['update']
    And  I change content of file 'dir/a' to '123'
    And  I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^'a' 'dir[/\\]a'$"
