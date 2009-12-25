import unittest
import re
from builder import *

class BuilderTests(unittest.TestCase):
    def test_simple_literals(self):
        self.assertEquals('ab', RegexBuilder().literal('ab').to_string())
    
    def test_chaining_literals(self):
        self.assertEquals('abc', RegexBuilder().literal('ab').literal('c').to_string())
    
    def test_escaping_literals(self):
        self.assertEquals('\.', RegexBuilder().literal('.').to_string())
    
    def test_raw(self):
        self.assertEquals('.', RegexBuilder().raw('.').to_string())
    
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

    def test_class(self):
        self.assertEquals('\d', RegexBuilder().class_('d').to_string())
    
    def test_or(self):
        self.assertEquals('a|b', RegexBuilder().alternate(literal('a'), literal('b')).to_string())
        self.assertEquals('(?:ab)|b', RegexBuilder().alternate(literal('ab'), literal('b')).to_string())
        self.assertEquals('a|(?:bc)', RegexBuilder().alternate(literal('a'), literal('bc')).to_string())
        self.assertEquals('(?:ab)|(?:cd)', RegexBuilder().alternate(literal('ab'), literal('cd')).to_string())
        self.assertEquals('a|bc', RegexBuilder().alternate(literal('a'), literal('b')).literal('c').to_string())
        self.assertEquals('(?:ab)|(?:cd)e', RegexBuilder().alternate(literal('ab'), literal('cd')).literal('e').to_string())
        self.assertEquals('ab|c', RegexBuilder().literal('a').alternate(literal('b'), literal('c')).to_string())
        self.assertEquals('(?:ab)|c', RegexBuilder().alternate(literal('ab'), literal('c')).to_string())
        self.assertEquals('a(?:b)|d+', RegexBuilder().one_or_more(alternate(literal('a').group('b', non_capture=True), literal('d'))).to_string())

    def test_optional(self):
        self.assertEquals('a?', RegexBuilder().optional(literal('a')).to_string())
        self.assertEquals('(?:ab)?', RegexBuilder().optional(literal('ab')).to_string())

    def test_immutible_objects(self):
        """ An object once built is immutible, any methods called on it do not change it """
        ab = RegexBuilder().literal('ab')
        self.assertEquals('abc', str(ab.literal('c')))
        self.assertEquals('abd+', str(ab.one_or_more('d')))
        self.assertEquals('abe*', str(ab.zero_or_more('e')))
        self.assertEquals('ab(f)', str(ab.group('f')))
        self.assertEquals('abg|h', str(ab.alternate('g', 'h')))
        self.assertEquals('abi{2}', str(ab.repeats('i', 2)))
        self.assertEquals('ab[j]', str(ab.range('j')))
        self.assertEquals('ab[^k]', str(ab.inverted_range('k')))
        self.assertEquals('ab', str(ab))

    def test_append(self):
        """ Append allows you to append a regex, and should explicitely allow you add yourself without error """
        ab = RegexBuilder().literal('ab')
        self.assertEquals('abab', str(ab.append(ab)))
        self.assertEquals('abcd', str(RegexBuilder().literal('ab').append('cd')))
        self.assertEquals('ab(?:cd)+', str(RegexBuilder().literal('ab').append(RegexBuilder().one_or_more(literal('cd')))))

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
        self.assertEquals(2, len(regex))
        self.assertEquals('a{1}', str(regex))
        regex = repeats(literal('a'),1,3)
        self.assertEquals(2, len(regex))
        self.assertEquals('a{1,3}', str(regex))

    def test_one_or_more(self):
        regex = one_or_more(literal('a'))
        self.assertEquals(2, len(regex))
        self.assertEquals('a+', str(regex))

    def test_zero_or_more(self):
        regex = zero_or_more(literal('a'))
        self.assertEquals(2, len(regex))
        self.assertEquals('a*', str(regex))

    def test_optional(self):
        regex = optional(literal('a'))
        self.assertEquals(2, len(regex))
        self.assertEquals('a?', str(regex))

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
        self.assertEquals(r'ac+d', literal('a').one_or_more(literal(r'c')).literal('d').to_string())
    def test_or_literal(self):
        regex = alternate(literal('a'),literal('b')).literal('c')
        self.assertEqual('a|bc', str(regex))
        self.assertNotEquals(None, re.match(str(regex), "ac"))
        self.assertNotEquals(None, re.match(str(regex), "bc"))
        regex = one_or_more(alternate(literal('a').group('b', non_capture=True), literal('d')))
        self.assertNotEquals(None, re.match(str(regex), "ab"))
        self.assertNotEquals(None, re.match(str(regex), "d"))
        self.assertEquals(None, re.match(str(regex), "ad"))
        self.assertNotEquals(None, re.match(str(regex), "abab"))
        self.assertNotEquals(None, re.match(str(regex), "dd"))
        self.assertNotEquals(None, re.match(str(regex), "dab"))

    def test_html_tag_parser(self):
        """ www.regular-expressions.info/examples.html - says this <TAG\b[^>]*>(.*?)</TAG> will match html tag TAG """
        regex = literal(r'<TAG').class_('b').zero_or_more(
                        inverted_range('>')
                    ).literal('>').group(
                        zero_or_more(
                            raw('.')), lazy=True
                    ).literal('</TAG>')
        self.assertEquals(
            r'\<TAG\b[^>]*\>(.*?)\<\/TAG\>', regex.to_string())
    def test_simple_ip_address(self):
        """ www.regular-expressions.info/examples.html - says this \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} will match tags """
        self.assertEquals(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', 
            repeats(class_('d'), 1, 3)
            .literal(r'.')
            .repeats(class_('d'), 1, 3)
            .literal(r'.')
            .repeats(class_('d'), 1, 3)
            .literal(r'.')
            .repeats(class_('d'), 1, 3)
            .to_string())

class RealLifeTests(unittest.TestCase):
    def test_section_keyword_urls(self):
        """ We want to match /travel/france, /travel/france+skiing, /travel/france+science/nanotechnology """
        slugword = one_or_more(range('a-zA-Z0-9'))
        section_keyword = slugword.literal('/').append(slugword)
        combiner = literal('/').append(section_keyword).optional(literal('+').alternate(section_keyword, slugword))
        regex = str(combiner)
        self.assertNotEqual(None, re.match(regex, "/travel/france"))
        self.assertNotEqual(None, re.match(regex, "/travel/france+skiing"))
        self.assertNotEqual(None, re.match(regex, "/travel/france+science/nanotechnology"))

class BugReportTests(unittest.TestCase):
    def test_bug_4_grouping_range(self):
        regex = one_or_more(literal('abc').range('a-z'))
        self.assertEquals("(?:abc[a-z])+", str(regex))
        regex = one_or_more(one_or_more(literal('a')))
        self.assertEquals("(?:a+)+", str(regex))
