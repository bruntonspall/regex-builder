import unittest
from builder import RegexBuilder

class BuilderTests(unittest.TestCase):
    def testSimpleLiterals(self):
        self.assertEquals('ab', RegexBuilder().literal('ab').to_string())
        
