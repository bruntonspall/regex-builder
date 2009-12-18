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

class StringAndLenTests(unittest.TestCase):
    def test_literal(self):
        regex = literal('ab')
        self.assertEquals(2, len(regex))
        self.assertEquals('ab', str(regex))
    
    def test_literal(self):
        regex = literal('ab').literal('c')
        self.assertEquals(3, len(regex))
        self.assertEquals('abc', str(regex))
    
    def test_repeats(self):
        regex = repeats(literal('a'),1)
        self.assertEquals(1, len(regex))
        self.assertEquals('a{1}', str(regex))
        regex = repeats(literal('a'),1,3)
        self.assertEquals(1, len(regex))
        self.assertEquals('a{1,3}', str(regex))

    def test_one_or_more(self):
        regex = one_or_more(literal('a'))
        self.assertEquals(1, len(regex))
        self.assertEquals('a+', str(regex))

    def test_zero_or_more(self):
        regex = zero_or_more(literal('a'))
        self.assertEquals(1, len(regex))
        self.assertEquals('a*', str(regex))

    def test_group(self):
        regex = group(literal('a'))
        self.assertEquals('(a)', str(regex))
        self.assertEquals(1, len(regex))

    def test_non_capture_group(self):
        regex = group(literal('a'), non_capture=True)
        self.assertEquals('(?:a)', str(regex))
        self.assertEquals(1, len(regex))

    def test_lazy_group(self):
        regex = group(literal('a'), lazy=True)
        self.assertEquals('(a?)', str(regex))
        self.assertEquals(1, len(regex))

    def test_lazy_non_capture_group(self):
        regex = group(literal('a'), non_capture=True, lazy=True)
        self.assertEquals('(?:a?)', str(regex))
        self.assertEquals(1, len(regex))

    def test_range(self):
        regex = range('abc')
        self.assertEquals('[abc]', str(regex))
        self.assertEquals(1, len(regex))

    def test_inverted_range(self):
        regex = inverted_range('abc')
        self.assertEquals('[^abc]', str(regex))
        self.assertEquals(1, len(regex))


class ComplexTests(unittest.TestCase):
    def test_one_or_more_multiword_literals(self):
        self.assertEquals('(?:bc)+', one_or_more(literal('bc')).to_string())
    def test_zero_or_more_multiword_literals(self):
        self.assertEquals('(?:bc)*', zero_or_more(literal('bc')).to_string())
    def test_repetition_of_multiword_literals(self):
        self.assertEquals('(?:bc){2,3}', repeats(literal('bc'), 2, 3).to_string())
    def test_one_or_more_single_character_literals(self):
        self.assertEquals(r'a\d+d', literal('a').one_or_more(literal(r'\d')).literal('d').to_string())
    def test_html_tag_parser(self):
        """ www.regular-expressions.info/examples.html - says this <TAG\b[^>]*>(.*?)</TAG> will match html tag TAG """
        regex = literal(r'<TAG\b').zero_or_more(
                        inverted_range('>')
                    ).literal('>').group(
                        zero_or_more(
                            literal('.')), lazy=True
                    ).literal('</TAG>')
        self.assertEquals(
            r'<TAG\b[^>]*>(.*?)</TAG>', regex.to_string())
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
