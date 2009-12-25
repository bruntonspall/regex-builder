import copy
import re

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
    def __str__(self):
        if self.next:
            return str(self.next)
        return ""
    def __len__(self):
        if self.next:
            return len(self.next)
        return 0

class LiteralNode(Node):
    def __str__(self):
        return Node.__str__(self)+str(self.data)
    def __len__(self):
        return Node.__len__(self)+len(str(self.data).replace('\\',''))
        
class RepeatsMinMaxNode(Node):
    def __str__(self):
        regex = self.data['regex']
        if len(regex) > 1:
            self.data['regex'] = group(regex, non_capture=True)
        return Node.__str__(self)+"%(regex)s{%(min)d,%(max)d}" % self.data
    def __len__(self):
        return len(self.data['regex'])+1

class RepeatsNumNode(Node):
    def __str__(self):
        regex = self.data['regex']
        if len(regex) > 1:
            self.data['regex'] = group(regex, non_capture=True)
        return Node.__str__(self)+"%(regex)s{%(num)d}" % self.data
    def __len__(self):
        return len(self.data['regex'])+1

class OneOrMoreNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s+" % str(self.data)
    def __len__(self):
        return len(self.data)+1

class ZeroOrMoreNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s*" % str(self.data)
    def __len__(self):
        return len(self.data)+1

class OptionalNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s?" % str(self.data)
    def __len__(self):
        return len(self.data)+1

class GroupNode(Node):
    def __str__(self):
        if self.data['lazy']:
            return Node.__str__(self)+"(%(regex)s?)" % self.data
        return Node.__str__(self)+"(%(regex)s)" % self.data
    def __len__(self):
        return len(self.data['regex'])

class NonCaptureGroupNode(Node):
    def __str__(self):
        if self.data['lazy']:
            return Node.__str__(self)+"(?:%(regex)s?)" % self.data
        return Node.__str__(self)+"(?:%(regex)s)" % self.data
    def __len__(self):
        return len(self.data['regex'])

class RangeNode(Node):
    def __str__(self):
        return Node.__str__(self)+"[%s]" % str(self.data)
    def __len__(self):
        return Node.__len__(self)+1

class InvertedRangeNode(Node):
    def __str__(self):
        return Node.__str__(self)+"[^%s]" % str(self.data)
    def __len__(self):
        return Node.__len__(self)+1

class OrNode(Node):
    def __str__(self):
        if len(self.data['lhs']) > 1:
            self.data['lhs'] = group(self.data['lhs'], non_capture=True)
        if len(self.data['rhs']) > 1:
            self.data['rhs'] = group(self.data['rhs'], non_capture=True)
        return Node.__str__(self)+"%(lhs)s|%(rhs)s" % self.data
    def __len__(self):
        return max(len(self.data['lhs']), len(self.data['rhs']))

class RegexBuilder:
    def __init__(self):
        self.text = ""
        self.len = 0
        self.root = Node()
        self.tail = self.root

    def __add_node(self, node):
        obj = copy.deepcopy(self)
        node.next = obj.root
        obj.root = node
        return obj

    def literal(self, lit):
        """ Adds a text literal to the regular expression. This escapes the literal """
        return self.__add_node(LiteralNode(re.escape(lit)))

    def raw(self, lit):
        """ Adds a text literal to the regular expression. This does not escape the literal """
        return self.__add_node(LiteralNode(lit))

    def repeats(self, regex, min, max=None):
        """ Repeats the passed expression n times """
        if max:
            return self.__add_node(RepeatsMinMaxNode({'min':min, 'max':max, 'regex': regex}))
        else:
            return self.__add_node(RepeatsNumNode({'num':min, 'regex': regex}))
    
    def group(self, regex, non_capture=False, lazy=False):
        """ Groups the passed regex with a backlink """
        if non_capture:
            return self.__add_node(NonCaptureGroupNode({'regex': regex, 'lazy': lazy}))
        else:
            return self.__add_node(GroupNode({'regex': regex, 'lazy': lazy}))

    def one_or_more(self, regex):
        """ Repeats the passed expression one or more times """
        return self.__add_node(OneOrMoreNode(regex))

    def zero_or_more(self, regex):
        """ Repeats the passed expression zero or more times """
        return self.__add_node(ZeroOrMoreNode(regex))
    
    def optional(self, regex):
        """ Makes the passed expression optional """
        return self.__add_node(OptionalNode(regex))
    
    def range(self, range):
        """ Matches any characters in the range """
        return self.__add_node(RangeNode(range))

    def inverted_range(self, range):
        """ Matches any characters in the range """
        return self.__add_node(InvertedRangeNode(range))

    def alternate(self, lhs, rhs):
        return self.__add_node(OrNode({'lhs':lhs, 'rhs':rhs}))

    def append(self, regex):
        return self.__add_node(copy.deepcopy(LiteralNode(regex)))

    def class_(self, classtype):
        return self.__add_node(copy.deepcopy(LiteralNode('\\'+classtype)))
        
    def to_string(self):
        """ DEPRECATED: use str(regex) instead """
        return str(self)

    def __str__(self):
        return str(self.root)

    def __len__(self):
        return len(self.root)

def literal(lit):
    """ Adds a text literal to the regular expression """
    return RegexBuilder().literal(lit)

def raw(lit):
    """ Adds a text literal to the regular expression """
    return RegexBuilder().raw(lit)

def class_(lit):
    """ Adds a text literal to the regular expression """
    return RegexBuilder().class_(lit)

def repeats(regex, min=None, max=None):
    """ Repeats the passed expression n times """
    return RegexBuilder().repeats(regex, min, max)

def group(regex, non_capture=False, lazy=False):
    """ Groups the passed regex with a backlink """
    return RegexBuilder().group(regex, non_capture, lazy)

def one_or_more(regex):
    """ Repeats the passed expression one or more times """
    return RegexBuilder().one_or_more(regex)

def zero_or_more(regex):
    """ Repeats the passed expression zero or more times """
    return RegexBuilder().zero_or_more(regex)

def optional(regex):
    """ The passed expression is optional """
    return RegexBuilder().optional(regex)

def range(lit):
    """ Matches any characters in the range """
    return RegexBuilder().range(lit)

def inverted_range(lit):
    """ Matches any characters NOT in the range """
    return RegexBuilder().inverted_range(lit)

def alternate(lhs, rhs):
    """ Matches either the lhs OR the rhs expressions """
    return RegexBuilder().alternate(lhs, rhs)
