Feature: run duplicates
  In order to process duplicates
  As a user
  I want to run commands on duplcate files

  Scenario: Run `run` in an non-empty initialized project
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 000     |
      | dir/b  | 123     |
      | dir/c  | 000     |
    When I run findd with ['update']
    And  I run findd with ['run', '-v', '--', 'python', '-c', 'import sys; f = open("RESULT.txt", "a"); f.write(" ".join(sys.argv[1:])); f.close()']
    Then the exit_code is zero
    And  the file contents of 'RESULT.txt' matches r"a dir/b"
    And  the file contents of 'RESULT.txt' matches r"dir/a dir/c"

  Scenario: Run `run` in an non-empty lazyily initialized project
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 000     |
      | dir/b  | 123     |
      | dir/c  | 000     |
    When I run findd with ['update', '--lazy']
    And  I run findd with ['run', '-v', '--', 'python', '-c', 'import sys; f = open("RESULT.txt", "a"); f.write(" ".join(sys.argv[1:])); f.close()']
    Then the exit_code is zero
    And  the file contents of 'RESULT.txt' matches r"a dir/b"
    And  the file contents of 'RESULT.txt' matches r"dir/a dir/c"

  Scenario: Run `run` in an non-empty initialized project skipping 2
    Given an initialized directory
    And containing files:
      | path   | content |
      | a      | 123     |
      | dir/a  | 123     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I run findd with ['run', '--skip=2', '-v', '--', 'python', '-c', 'import sys; f = open("RESULT.txt", "a"); f.write(" ".join(sys.argv[1:])); f.close()']
    Then the exit_code is zero
    And  the file contents of 'RESULT.txt' matches r"dir/b"

  Scenario: Run `run` in a subdirectory
    Given an initialized directory
    And containing files:
      | path   | content |
      | cwd/a  | 123     |
      | dir/b  | 123     |
    When I run findd with ['update']
    And  I run findd with ['run', '-v', '--', 'python', '-c', 'import os; import sys; f = open("RESULT.txt", "a"); f.write(str(os.path.exists(sys.argv[1])) + ":" + sys.argv[1]); f.close()'] in 'cwd'
    Then the exit_code is zero
    And  the file contents of 'RESULT.txt' matches r"True:"
