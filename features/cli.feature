Feature: command line interface
  In order to find duplicates
  As a cli user
  I want to use the cli

  Scenario: I need to be aware of '-h'
    When  I run findd with None
    Then the exit_code is non-zero
    And  the stderr_capture matches '\[-h\]'

  Scenario: I need help
    When  I run findd with ['--help']
    Then the exit_code is zero
    And  the stdout_capture matches '[Rr]eport .* bugs to.*http.*findd'
    And  the stdout_capture matches '[Hh]ome page.*http.*findd'
