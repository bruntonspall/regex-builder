class RegexBuilder:
    def __init__(self):
        self.text = ""
    def literal(self, lit):
        self.text += lit
        return self
    def to_string(self):
        return self.text
