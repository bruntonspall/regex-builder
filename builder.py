class RegexBuilder:
    def __init__(self):
        self.text = ""
        self.len = 0

    def literal(self, lit):
        """ Adds a text literal to the regular expression """
        self.text += lit
        self.len += len(lit.replace('\\', ''))
        return self

    def repeats(self, regex, min, max=None):
        """ Repeats the passed expression n times """
        if max:
            self.text += self.__group_and_append(regex, '{%d,%d}' % (min, max))
        else:
            self.text += self.__group_and_append(regex, '{%d}' % (min))
        self.len += len(regex)
        return self
    
    def group(self, regex, non_capture=False, lazy=False):
        """ Groups the passed regex with a backlink """
        pre = ''
        post = ''
        if non_capture:
            pre = '?:'
        if lazy:
            post = '?'
        self.text += "(%s%s%s)" % (pre, regex.to_string(), post)
        self.len += len(regex)
        return self

    def one_or_more(self, regex):
        """ Repeats the passed expression one or more times """
        self.text += self.__group_and_append(regex, '+')
        self.len += len(regex)
        return self

    def zero_or_more(self, regex):
        """ Repeats the passed expression zero or more times """
        self.text += self.__group_and_append(regex, '*')
        self.len += len(regex)
        return self
    
    def range(self, range):
        """ Matches any characters in the range """
        self.text += "[%s]" % (range)
        self.len += 1
        return self

    def inverted_range(self, range):
        """ Matches any characters in the range """
        self.text += "[^%s]" % (range)
        self.len += 1
        return self

    def __group_and_append(self, regex, lit):
        r = regex.to_string()
        if len(regex) > 1:
            r = "(?:%s)" % (r)
        return "%s%s" % (r,lit)
        

    def to_string(self):
        return self.text

    def __len__(self):
        return self.len

def literal(lit):
    return RegexBuilder().literal(lit)

def repeats(regex, min=None, max=None):
    return RegexBuilder().repeats(regex, min, max)

def group(regex, non_capture=False):
    return RegexBuilder().group(regex, non_capture)

def one_or_more(regex):
    return RegexBuilder().one_or_more(regex)

def zero_or_more(regex):
    return RegexBuilder().zero_or_more(regex)

def range(lit):
    return RegexBuilder().range(lit)

def inverted_range(lit):
    return RegexBuilder().inverted_range(lit)
