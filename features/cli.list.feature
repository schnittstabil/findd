Feature: list duplicates
  In order to find duplicates
  As a user
  I want to list all duplicates tracked by findd

  Scenario: Run `list` in uninitialized project
    Given an uninitialized directory
    When  I run findd with ['list']
    Then  the exit_code is non-zero

  Scenario: Run `list` in an empty initialized project
    Given an initialized directory
    When I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches "^$"

  Scenario: Run `list` in an non-empty initialized project
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 000     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^a dir[/\\]b$"

  Scenario: Run `list` in an initialized project containing only duplicates
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^a dir[/\\]b$"

  Scenario: Run `list` in a subdirectory
    Given an initialized directory
    And containing files:
      | path   | content |
      | cwd/a  | 123     |
      | dir/b  | 123     |
    When I run findd with ['update'] in 'cwd'
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^a ..[/\\]dir[/\\]b$"

  Scenario: Run `list` in an initialized project containing duplicates with wrong encoded names
    Given an initialized directory
    And containing files:
      | path                | content |
      | a                   | 123     |
      | dir/wrong�encoded   | 123     |
      | dir/wrong¦encoded2  | 123     |
    When I run findd with ['update']
    And  I run findd with ['list']
    Then the exit_code is zero
    And  the stdout_capture matches r"^a 'dir[/\\]wrong.encoded2?' 'dir[/\\]wrong.encoded2?'$"

  Scenario: Pipe `list` with wrong encoded names
    Given an initialized directory
    And containing files:
      | path                | content |
      | a                   | 123     |
      | dir/wrong�encoded   | 123     |
      | dir/wrong¦encoded2  | 123     |
    When I run findd with ['update']
    And  I run 'python {FINDD} list | wc -l' in a shell
    Then the stderr_capture_ matches r"^$"
    And  the stdout_capture_ matches r"^1$"
    And  the exit_code is zero

  Scenario: Run `list` and broken Pipe
    Given an initialized directory
    And containing files:
      | path                | content |
      | a                   | 123     |
      | dir/wrong�encoded   | 123     |
      | dir/wrong¦encoded2  | 123     |
    When I run findd with ['update']
    And  I run 'python {FINDD} list | python -c "print(True)"' in a shell
    Then the stderr_capture_ matches r"^$"
    And  the stdout_capture_ matches r"^True$"
    And  the exit_code is zero

  Scenario: Run `list` but limit results
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/b  | 123     |
      | c      | 42      |
      | dir/d  | 42      |
    When I run findd with ['update']
    And  I run findd with ['list', '--limit', '1']
    Then the exit_code is zero
    And  the stdout_capture matches r"^a dir[/\\]b$"

  Scenario: Run `list` but limit=0 results in empty output
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I run findd with ['list', '--limit', '0']
    Then the exit_code is zero
    And  the stdout_capture matches r"^$"
