Feature: debug findd
  In order to debug findd
  As a developer
  I want to use the findd package

  Scenario: verify findd installation
    When I import the findd package
    Then the findd package __version__ value exists
