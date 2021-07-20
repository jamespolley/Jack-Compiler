# TO DO: fix bug where last token is ignored, or character immediately after is ignored

class Tokenizer:

    # to do - set token type when get_next_token() is called
    KEYWORD = 0
    IDENTIFIER = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4

    SYMBOLS = r"{}()[].,+-*/&|<>=~"
    KEYWORDS = [
        "class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true","false", "null", "this", "let", "do", "if", "else", "while", "return"]

    def __init__(self, file):
        self.file = file
        self.i = 0
        self.length = len(self.file)
        self.token = None
        self.token_type = None # to implement
        
    
    def advance(self):
        self.token = None
        while (self.token == None) and self.has_more_chars():
            # Ignore whitespace and comments
            if self.file[self.i] == " ": pass
            elif self.file[self.i : self.i+2] == "//":
                self.ignore_line_comment()
            elif self.file[self.i : self.i+2] == "/*":
                self.ignore_open_close_comment()
            
            # Process words (keyword or identifier)
            elif self.file[self.i].isidentifier():
                self.process_keyword_or_identifier()

            # Process symbols
            elif self.file[self.i] in self.SYMBOLS:
                self.process_symbol()

            # Process constants
            elif self.file[self.i].isdigit():
                self.process_integer_constant()
            elif self.file[self.i] == '"':
                self.process_string_constant()
            
            else:
                # print(self.file[self.i])
                pass
            self.i += 1

    
    def has_more_chars(self):
        return self.i < self.length
    
    def ignore_line_comment(self):
        self.i += 2
        while self.has_more_chars():
            if self.file[self.i] == "\n":
                return
            self.i += 1

    def ignore_open_close_comment(self):
        self.i += 2
        while self.has_more_chars():
            if self.file[self.i : self.i+2] == "*/":
                self.i += 1
                return
            self.i += 1
    
    def process_keyword_or_identifier(self):
        # Refactor???
        start = self.i
        while self.has_more_chars():
            if not self.file[start : self.i+2].isidentifier(): break
            self.i += 1
        self.token = self.file[start : self.i+1]
        if self.token in self.KEYWORDS: self.token_type = self.KEYWORD
        else: self.token_type = self.IDENTIFIER

    def process_symbol(self):
        self.token = self.file[self.i]
        self.token_type = self.SYMBOL
        self.i += 1

    def process_integer_constant(self):
        start = self.i
        self.i += 1
        while self.has_more_chars():
            if not self.file[self.i].isdigit():
                break
            self.i += 1
        self.token = self.file[start : self.i]
        self.token_type = self.INT_CONSTANT

    def process_string_constant(self):
        start = self.i
        self.i += 1
        while self.has_more_chars():
            if self.file[self.i] == '"':
                self.i += 1
                self.token = self.file[start : self.i]
                self.token_type = self.STRING_CONSTANT
                return
            self.i += 1
        raise Exception("Unexpected end of file: expected to read '\"'")
        





# Test
t = Tokenizer(' asdff_{}34- //    \n asdff9 "token"  445   /* asdf 99 */ qwer "last_token"{} 999 asdf')

while t.has_more_chars():
    t.advance()
    print(t.token)
    print(t.token_type)
