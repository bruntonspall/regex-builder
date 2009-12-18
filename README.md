Regex Builder
=============

A simple regex builder python interface, making describing complicated regular expressions slightly easier to understand
Licensed under BSD License, see LICENSE.txt for details.

Features
--------

 * Chaining API
 * Easy to use

API
---

### method builders

These can be imported from the library as functions, and chained as normal.
They return a RegexBuilder object, so do to_string if you want to feed it into the re module

    from regex_builder import *
    regex = str(repeats(literal('a'),2,3))
    assertEquals('a{2,3}', regex)

 * _literal_ returns a literal string to be used in the regex.  Be careful of backslash characters
 * _repeats_ takes another regex and either fixed number of repeats, or a minimum and maximum
 * _group_ takes another regex, and creates a matching group.  use non_capture=True for non-capturing groups
 * _one_or_more_ takes a regex and adds the '+' repeat token
 * _zero_or_more_ takes a regex and adds the '*' repeat token
 * _range_ takes a literal, and turns it into a character range, i.e. abc => [abc]
 * _inverted_range_ takes a literal and turns it into an inverted chaarcter range, i.e. abc => [^abc]


