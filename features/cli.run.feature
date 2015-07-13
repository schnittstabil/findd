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
    When I run findd with ['update']
    And  I run findd with ['run', '--', 'python', '-c', 'import sys; f = open("RESULT.txt", "w"); f.write(" ".join(sys.argv[1:])); f.close()']
    Then the exit_code is zero
    And  the file contents of 'RESULT.txt' matches r"a dir/b"
