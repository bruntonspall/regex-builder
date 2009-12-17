import unittest
import re
from builder import *

class BuilderTests(unittest.TestCase):
    def test_simple_literals(self):
        self.assertEquals('ab', RegexBuilder().literal('ab').to_string())
    
    def test_chaining_literals(self):
        self.assertEquals('abc', RegexBuilder().literal('ab').literal('c').to_string())
    
    def test_repetition(self):
        self.assertEquals('a{2}', RegexBuilder().repeats(RegexBuilder().literal('a'), 2).to_string())
    
    def test_repetition_maximum(self):
        self.assertEquals('a{2,3}', RegexBuilder().repeats(RegexBuilder().literal('a'), 2, 3).to_string())

    def test_group(self):
        self.assertEquals('a(b)', RegexBuilder().literal('a').group(RegexBuilder().literal('b')).to_string())

    def test_non_capturing_group(self):
        self.assertEquals('a(?:b)', RegexBuilder().literal('a').group(RegexBuilder().literal('b'), non_capture=True).to_string())

    def test_repetition_one_or_more(self):
        self.assertEquals('ab+', RegexBuilder().literal('a').one_or_more(RegexBuilder().literal('b')).to_string())
    
    def test_repetition_zero_or_more(self):
        self.assertEquals('ab*', RegexBuilder().literal('a').zero_or_more(RegexBuilder().literal('b')).to_string())

    def test_character_range(self):
        self.assertEquals('[abc]', RegexBuilder().range('abc').to_string())
    
    def test_character_inverted_range(self):
        self.assertEquals('[^abc]', RegexBuilder().inverted_range('abc').to_string())
    
    def test_module_functions(self):
        self.assertEquals('ab(c{3,7})d', literal('ab').group(repeats(literal('c'), 3, 7)).literal('d').to_string())

class ComplexTests(unittest.TestCase):
    def test_one_or_more_multiword_literals(self):
        self.assertEquals('a(?:bc)+d', literal('a').one_or_more(literal('bc')).literal('d').to_string())
    def test_zero_or_more_multiword_literals(self):
        self.assertEquals('a(?:bc)*d', literal('a').zero_or_more(literal('bc')).literal('d').to_string())
    def test_repetition_of_multiword_literals(self):
        self.assertEquals('a(?:bc){2,3}d', literal('a').repeats(literal('bc'), 2, 3).literal('d').to_string())
    def test_one_or_more_single_character_literals(self):
        self.assertEquals(r'a\d+d', literal('a').one_or_more(literal(r'\d')).literal('d').to_string())
    def test_html_tag_parser(self):
        """ www.regular-expressions.info/examples.html - says this <TAG\b[^>]*>(.*?)</TAG> will match html tag TAG """
        self.assertEquals(
            r'<TAG\b[^>]*>(.*?)</TAG>', 
            literal(r'<TAG\b')
            .zero_or_more(
                inverted_range('>'))
            .literal('>')
            .group(
                zero_or_more(
                    literal('.')), lazy=True)
            .literal('</TAG>')
            .to_string())
    def test_simple_ip_address(self):
        """ www.regular-expressions.info/examples.html - says this \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} will match tags """
        self.assertEquals(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', 
            repeats(literal(r'\d'), 1, 3)
            .literal(r'\.')
            .repeats(literal(r'\d'), 1, 3)
            .literal(r'\.')
            .repeats(literal(r'\d'), 1, 3)
            .literal(r'\.')
            .repeats(literal(r'\d'), 1, 3)
            .to_string())
