# TO DO - include grammar in docstrings

from Tokenizer import Tokenizer


class CompilationEngineXML:
    KEYWORD = 0
    IDENTIFIER = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4

    TAGS = ["keyword", "identifier", "symbol",
        "integerConstant", "stringConstant"]
    
    OP = "+-*/=&|<>"
    UNARY_OP = "-~"

    KEYWORD_CONSTANT = ("true", "false", "null", "this")
    
    def __init__(self, file):
        self.tokenizer = Tokenizer(file)
        self.xml = []
        self.tab_level = 0
    
    def compile(self):
        while self.tokenizer.has_more_chars():
            self.tokenizer.advance()
            self.compile_class()
        print(self.xml)
    
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
        self.expect(("constructor", "function", "method"))
        self.expect(("void", "int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)
        self.expect("(")
        self.compile_parameter_list()
        self.expect(")")
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
        """
        Compile a variable declaration.
        """
        if self.tokenizer.token != "var": return
        self.open_tag("varDec")
        self.expect("var")
        self.expect(("int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)
        while self.tokenizer.token == ",":
            self.expect(",")
            self.expect(self.IDENTIFIER)
        self.expect(";")
        self.close_tag("varDec")
        self.compile_var_dec()

    def compile_statements(self):
        """Compile a sequence of statements. Does not handle the enclosing "{}"."""
        self.open_tag("statements")
        token = self.tokenizer.token
        has_more_statements = True
        while has_more_statements:
            if token == "let": self.compile_let_statement()
            elif token == "if": self.compile_if_statement()
            elif token == "while": self.compile_while_statement()
            elif token == "do": self.compile_do_statement()
            elif token == "return": self.compile_return_statement()
            else: has_more_statements = False
        self.close_tag("statements")

    def compile_let_statement(self):
        """
        Compile a let statement.

        'let' varName ( '[' expression ']')? '=' expression ';'
        """
        self.open_tag("letStatement")
        self.expect("let")
        self.expect(self.IDENTIFIER)
        if self.tokenizer.token == "[":
            self.expect("[")
            self.compile_expression()
            self.expect("]")
        self.expect("=")
        self.compile_expression()
        self.expect(";")
        self.close_tag("letStatement")

    def compile_if_statement(self):
        """
        Compile an if statement.
        """
        self.open_tag("ifStatement")
        self.expect("if")
        self.expect("(")
        self.compile_expression()
        self.expect(")")
        self.expect("{")
        self.compile_statements()
        self.expect("}")
        if self.tokenizer.token == "else":
            self.expect("else")
            self.expect("{")
            self.compile_statements()
            self.expect("}")
        self.close_tag("ifStatement")

    def compile_while_statement(self):
        """
        Compile a while statement.
        """
        self.open_tag("whileStatement")
        self.expect("while")
        self.expect("(")
        self.compile_expression()
        self.expect(")")
        self.expect("{")
        self.compile_statements()
        self.expect("}")
        self.close_tag("whileStatement")

    def compile_do_statement(self):
        """Compile a do statement."""
        self.open_tag("doStatement")
        self.expect("do")
        self.expect(self.IDENTIFIER)
        if self.tokenizer.token == ".":
            self.expect(".")
            self.expect(self.IDENTIFIER)
        self.expect("(")
        self.compile_expression_list()
        self.expect(")")
        self.expect(";")
        self.close_tag("doStatement")

    def compile_return_statement(self):
        """Compile a return statement."""
        self.open_tag("returnStatement")
        self.expect("return")
        self.compile_expression_list()
        self.expect(";")
        self.close_tag("returnStatement")

    def compile_expression(self):
        """Compile an expression."""
        success = self.compile_term()
        while self.tokenizer.token in self.OP:
            self.expect(self.OP)
            self.compile_term()
        return success

    def compile_term(self):
        """Compile a term. If the current token is an identifier, distinguishes between a variable, an array entry, or a subroutine call."""
        token = self.tokenizer.token
        token_type = self.tokenizer.token_type
        if token_type == self.INT_CONSTANT:
            self.expect(self.INT_CONSTANT)
        elif token_type == self.STRING_CONSTANT:
            self.expect(self.STRING_CONSTANT)
        elif token_type in self.KEYWORD_CONSTANT:
            self.expect(self.KEYWORD)
        elif token_type == self.IDENTIFIER:
            self.expect(self.IDENTIFIER)
            # In case of subroutine call
            # BELOW CAN BE SIMPLIFIED WITHOUT LOSING FUNCTIONALITY???
            if self.tokenizer.token == ".":
                self.expect(".")
                self.expect(self.IDENTIFIER)
                self.expect("(")
                self.compile_expression_list()
                self.expect(")")
            elif self.tokenizer.token == "(":
                self.expect("(")
                self.compile_expression_list()
                self.expect(")")
            return
        elif token == "(":
            self.expect("(")
            self.compile_expression()
            self.expect(")")
        elif token == "{":
            self.expect("{")
            self.compile_expression()
            self.expect("}")
        elif token in self.UNARY_OP:
            self.expect(self.UNARY_OP)
            self.compile_term()
        else:
            return False # NOT A TERM
            # raise Exception() # TO DO ----------
        return True

    def compile_expression_list(self):
        """Compile a (possibly empty) comma-separated list of expressions."""
        # TO DO - XML tags
        success = self.compile_expression() # is this necessary further up the chain???
        while self.tokenizer.token == ",":
            self.expect(",")
            self.compile_expression()

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
        elif token == None: return # End of File
        elif token != expected:
            raise Exception() # TO DO ----------
        
        self.open_close_tag(self.TAGS[token_type], token)
        print(self.tokenizer.token)
        print(self.tokenizer.token_type)
        self.tokenizer.advance()
        print(self.xml)

    def open_tag(self, tag_name):
        self.xml.append("\t"*self.tab_level)
        self.xml.append("<{}>\n".format(tag_name))
        self.tab_level += 1
    
    def close_tag(self, tag_name):
        self.tab_level -= 1
        self.xml.append("\t"*self.tab_level)
        self.xml.append("</{}>\n".format(tag_name))
    
    def open_close_tag(self, tag_name, value=""):
        if value != "": value = " " + value
        self.xml.append("\t"*self.tab_level)
        self.xml.append("<{0}>{1} </{0}>\n".format(tag_name, value))

# test
ja = CompilationEngineXML('class Main { function void main(){var Array a; var int length; var int i, sum;}}')
ja.compile()
