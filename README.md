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

 * _literal(string)_ returns a literal string to be used in the regex.  Be careful of backslash characters
 * _range(string)_ takes a literal, and turns it into a character range, i.e. abc => [abc]
 * _inverted_range(string)_ takes a literal and turns it into an inverted chaarcter range, i.e. abc => [^abc]
 * _repeats(regex)_ takes another regex and either fixed number of repeats, or a minimum and maximum
 * _group(regex)_ takes another regex, and creates a matching group.  use non_capture=True for non-capturing groups
 * _one_or_more(regex)_ takes a regex and adds the '+' repeat token
 * _zero_or_more(regex)_ takes a regex and adds the '*' repeat token
 * _optional(regex)_ makes the passed regex optional
 * _append(regex)_ takes a regex and appends it to your regex.

### Shortcuts

There are a few shortcuts that are handy.

 * Any method that takes a regex can also take a string, for example one_or_more('ab') returns '(?:ab)+'
 * The Builder objects are immutable, so you can store them and reuse them, for example, ab= literal('ab'); 'abc' == ab.literal('c'); 'abd' == ab.literal('d')

### Examples

There are some examples in the unit testing framework, but here are some extra
   from regex_builder import *
   number = optional(range('1-2')).optional(range('0-9')).range('0-9')
   dotted_number = number.literal('\\.')
   ip_addr = repeats(dotted_number, 3).append(dotted_number)


