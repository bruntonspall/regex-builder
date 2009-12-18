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
        return Node.__str__(self)+self.data
    def __len__(self):
        return Node.__len__(self)+len(self.data.replace('\\',''))
        
class RepeatsMinMaxNode(Node):
    def __str__(self):
        regex = self.data['regex']
        if len(regex) > 1:
            self.data['regex'] = group(regex, non_capture=True)
        return Node.__str__(self)+"%(regex)s{%(min)d,%(max)d}" % self.data
    def __len__(self):
        return len(self.data['regex'])

class RepeatsNumNode(Node):
    def __str__(self):
        regex = self.data['regex']
        if len(regex) > 1:
            self.data['regex'] = group(regex, non_capture=True)
        return Node.__str__(self)+"%(regex)s{%(num)d}" % self.data
    def __len__(self):
        return len(self.data['regex'])

class OneOrMoreNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s+" % str(self.data)
    def __len__(self):
        return len(self.data)

class ZeroOrMoreNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s*" % str(self.data)
    def __len__(self):
        return len(self.data)

class OptionalNode(Node):
    def __str__(self):
        if len(self.data) > 1:
            self.data = group(self.data, non_capture=True)
        return Node.__str__(self)+"%s?" % str(self.data)
    def __len__(self):
        return len(self.data)

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
        return 1

class InvertedRangeNode(Node):
    def __str__(self):
        return Node.__str__(self)+"[^%s]" % str(self.data)
    def __len__(self):
        return 1

class OrNode(Node):
    def __str__(self):
        if len(self.data['lhs']) > 1:
            self.data['lhs'] = group(self.data['lhs'], non_capture=True)
        if len(self.data['rhs']) > 1:
            self.data['rhs'] = group(self.data['rhs'], non_capture=True)
        return Node.__str__(self)+"%(lhs)s|%(rhs)s" % self.data
    def __len__(self):
        return 1

class RegexBuilder:
    def __init__(self):
        self.text = ""
        self.len = 0
        self.root = Node()
        self.tail = self.root

    def __insert_node(self, node):
        node.next = self.root
        self.root = node

    def literal(self, lit):
        """ Adds a text literal to the regular expression """
        self.__insert_node(LiteralNode(lit))
        return self

    def repeats(self, regex, min, max=None):
        """ Repeats the passed expression n times """
        if max:
            self.__insert_node(RepeatsMinMaxNode({'min':min, 'max':max, 'regex': regex}))
        else:
            self.__insert_node(RepeatsNumNode({'num':min, 'regex': regex}))
        return self
    
    def group(self, regex, non_capture=False, lazy=False):
        """ Groups the passed regex with a backlink """
        if non_capture:
            self.__insert_node(NonCaptureGroupNode({'regex': regex, 'lazy': lazy}))
        else:
            self.__insert_node(GroupNode({'regex': regex, 'lazy': lazy}))
        return self

    def one_or_more(self, regex):
        """ Repeats the passed expression one or more times """
        self.__insert_node(OneOrMoreNode(regex))
        return self

    def zero_or_more(self, regex):
        """ Repeats the passed expression zero or more times """
        self.__insert_node(ZeroOrMoreNode(regex))
        return self
    
    def optional(self, regex):
        """ Makes the passed expression optional """
        self.__insert_node(OptionalNode(regex))
        return self
    
    def range(self, range):
        """ Matches any characters in the range """
        self.__insert_node(RangeNode(range))
        return self

    def inverted_range(self, range):
        """ Matches any characters in the range """
        self.__insert_node(InvertedRangeNode(range))
        return self

    def alternate(self, lhs, rhs):
        self.__insert_node(OrNode({'lhs':lhs, 'rhs':rhs}))
        return self

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
