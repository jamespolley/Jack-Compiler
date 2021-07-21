from Tokenizer import Tokenizer


class CompilationEngineXML:
    KEYWORD = 0
    IDENTIFIER = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4

    TAGS = ["keyword", "identifier", "symbol",
        "integerConstant", "stringConstant"]
    

    def __init__(self, file):
        self.tokenizer = Tokenizer(file)
        self.xml = []
        self.tab_level = 0
    
    def compile(self):
        while self.tokenizer.has_more_chars():
            self.tokenizer.advance()
            print(self.tokenizer.token)
            self.compile_class()
    
    def compile_class(self):
        """
        Compile a complete class.

        'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.open_tag("class")
        self.expect("class")
        self.expect(self.IDENTIFIER)
        self.expect('{')
        self.compile_class_var_dec()
        self.compile_subroutine_dec()
        self.expect('}')
        self.close_tag("class")
        
    def compile_class_var_dec(self):
        """
        Compile a static variable declaration, or a field declaration.
        """
        # OPTIONAL classVarDec
        if not self.tokenizer.token in ("static", "field"): return
        
        self.open_tag("classVarDec")
        self.expect(("static", "field"))
        self.expect(("int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)

        while self.tokenizer.token == ",":
            self.expect(",")
            self.expect(self.IDENTIFIER)

        self.expect(";")
        self.close_tag("classVarDec")
        self.compile_class_var_dec() # for multiple classVarDec

    def compile_subroutine_dec(self):
        """
        Compile a complete method, function, or constructor.
        """
        # OPTIONAL subroutineDec
        if not self.tokenizer.token in \
        ("constructor", "function", "method"):
            return
        self.open_tag("subroutineDec")

        # ('constructor' | 'function' | 'method')
        self.open_close_tag("keyword", self.tokenizer.token)
        self.tokenizer.advance()

        # type:     ('void' | 'int' | 'char' | 'boolean' | className)
        self.open_close_tag("keyword", self.tokenizer.token)
        self.tokenizer.advance()

        # subroutineName
        self.open_close_tag("identifier", self.tokenizer.token)
        self.tokenizer.advance()

        self.expect("(")

        # parameterList
        self.compile_parameter_list()

        self.expect(")")

        # subroutineBody
        self.compile_subroutine_body()

        self.close_tag("subroutineDec")

    def compile_parameter_list(self):
        """
        Compile a (possibly empty) parameter list. Does not handle the enclosing "()".

        ( (type varName) (',' type varName)* )?
        """
        if not self.tokenizer.token_type in \
        (self.KEYWORD, self.IDENTIFIER):
            self.open_close_tag(self.TAGS[self.tokenizer.token_type])
            return # TO DO ---------- method for determining if a type?
        self.open_tag("parameterList")
        self.expect(("int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)
        while self.tokenizer.token == ",":
            self.expect(",")
            self.expect(("int", "char", "boolean")) # OR className
            self.expect(self.IDENTIFIER)
        self.close_tag("parameterList")

    def compile_subroutine_body(self):
        """
        Compile a subroutine's body.
        """
        self.open_tag("subroutineBody")
        self.expect("{")
        self.compile_var_dec() # TO DO -----
        self.compile_statements() # TO DO -----
        self.expect("}")
        self.close_tag("subroutineBody")

    def compile_var_dec(self):
        # Compile a variable declaration.
        pass

    def compile_statements(self):
        # Compile a sequence of statements. Does not handle the
        # enclosing "{}".
        pass

    def compile_expression(self):
        # Compile an expression.
        pass

    def compile_term(self):
        # Compile a term. If the current token is an identifier,
        # distinguishes between a variable, an array entry, or a
        # subroutine call.
        pass

    def compile_expression_list(self):
        # Compile a (possibly empty) comma-separated list of
        # expressions.
        pass




    def expect(self, expected):
        token = self.tokenizer.token
        token_type = self.tokenizer.token_type

        if type(expected) is tuple:
            if not token in expected:
                if token_type != self.IDENTIFIER:
                    raise Exception() # TO DO ----------
        elif type(expected) is int:
            if not token_type == expected:
                raise Exception() # TO DO ----------
        elif token != expected:
            raise Exception() # TO DO ----------
        
        self.open_close_tag(self.TAGS[token_type], token)
        self.tokenizer.advance()
        print(self.xml)

    def open_tag(self, tag_name):
        for i in range(self.tab_level):
            self.xml.append("\t")
        self.xml.append("<{}>".format(tag_name))
        self.xml.append("\n")
        self.tab_level += 1
    
    def close_tag(self, tag_name):
        self.tab_level -= 1
        for i in range(self.tab_level):
            self.xml.append("\t")
        self.xml.append("</{}>".format(tag_name))
        self.xml.append("\n")
    
    def open_close_tag(self, tag_name, value=""):
        if value != "": value = value + " "
        for i in range(self.tab_level):
            self.xml.append("\t")
        self.xml.append("<{0}>{1} </{0}>".format(tag_name, value))
        self.xml.append("\n")


# test
ja = CompilationEngineXML('class Main { function void main(){var Array a; var int length; var int i, sum;}')
ja.compile()