# TO DO
#   In compile_expression(), any other expression exits??
#   Move constants/codes to new file
#   " should be &quot; ?????
from Tokenizer import Tokenizer


class ParserXML:
    """
    Receives tokens from the Tokenizer, identifies grammar, and generates XML.
    """

    KEYWORD = 0
    IDENTIFIER = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4

    TAGS = ["keyword", "identifier", "symbol",
        "integerConstant", "stringConstant"]
    
    OP = ("+", "-", "*", "/", "=", "&", "|", "<", ">")
    UNARY_OP = ("-", "~")

    KEYWORD_CONSTANT = ("true", "false", "null", "this")
    
    def __init__(self, file):
        self.tokenizer = Tokenizer(file)
        self.xml = []
        self.tab_level = 0
    
    def compile(self):
        """Compiles Jack code into XML code (which identifies its lexical elements and grammar)."""
        self.tokenizer.advance()
        while self.tokenizer.has_more_chars():
            self.compile_class()
    
    def compile_class(self):
        """Compiles a complete class."""
        self.open_tag("class")
        self.expect("class")
        self.expect(self.IDENTIFIER)
        self.expect('{')
        self.compile_class_var_dec()
        self.compile_subroutine_dec()
        self.expect('}')
        self.close_tag("class")
        
    def compile_class_var_dec(self):
        """Compiles a static variable declaration, or a field declaration."""
        if not self.tokenizer.token in ("static", "field"):
            return # classVarDec is optional
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
        """Compiles a complete method, function, or constructor."""
        if not self.tokenizer.token in \
        ("constructor", "function", "method"):
            return # subroutineDec is optional
        self.open_tag("subroutineDec")
        self.expect(("constructor", "function", "method"))
        self.expect(("void", "int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)
        self.expect("(")
        self.compile_parameter_list()
        self.expect(")")
        self.compile_subroutine_body()
        self.close_tag("subroutineDec")
        self.compile_subroutine_dec() # for multiple classVarDec

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list. Does not handle the enclosing "()"."""
        self.open_tag("parameterList")
        if self.tokenizer.token != ")":
            self.expect(("int", "char", "boolean")) # OR className
            self.expect(self.IDENTIFIER)
            while self.tokenizer.token == ",":
                self.expect(",")
                self.expect(("int", "char", "boolean")) # OR className
                self.expect(self.IDENTIFIER)
        self.close_tag("parameterList")

    def compile_subroutine_body(self):
        """Compiles a subroutine's body."""
        self.open_tag("subroutineBody")
        self.expect("{")
        self.compile_var_dec()
        self.compile_statements()
        self.expect("}")
        self.close_tag("subroutineBody")

    def compile_var_dec(self):
        """Compiles a variable declaration."""
        if self.tokenizer.token != "var":
            return # varDec is optional
        self.open_tag("varDec")
        self.expect("var")
        self.expect(("int", "char", "boolean")) # OR className
        self.expect(self.IDENTIFIER)
        while self.tokenizer.token == ",":
            self.expect(",")
            self.expect(self.IDENTIFIER)
        self.expect(";")
        self.close_tag("varDec")
        self.compile_var_dec() # for multiple varDec

    def compile_statements(self):
        """Compiles a sequence of statements. Does not handle the enclosing "{}"."""
        self.open_tag("statements")
        while True:
            token = self.tokenizer.token
            if token == "let": self.compile_let_statement()
            elif token == "if": self.compile_if_statement()
            elif token == "while": self.compile_while_statement()
            elif token == "do": self.compile_do_statement()
            elif token == "return": self.compile_return_statement()
            else: break
        self.close_tag("statements")

    def compile_let_statement(self):
        """Compiles a let statement."""
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
        """Compiles an if statement."""
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
        """Compiles a while statement."""
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
        """Compiles a do statement."""
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
        """Compiles a return statement."""
        self.open_tag("returnStatement")
        self.expect("return")
        if self.tokenizer.token != ";":
            self.compile_expression()
        self.expect(";")
        self.close_tag("returnStatement")

    def compile_expression(self):
        """Compiles an expression."""
        if self.tokenizer.token in ";)]":
            return # expression is optional
        self.open_tag("expression")
        self.compile_term()
        while self.tokenizer.token in self.OP:
            token = self.tokenizer.token
            if token == "<": self.expect_special("&lt;")
            elif token == ">": self.expect_special("&gt;")
            elif token == "&": self.expect_special("&amp;")
            else: self.expect(self.OP)
            self.compile_term()
        self.close_tag("expression")

    def compile_term(self):
        """Compiles a term. If the current token is an identifier, distinguishes between a variable, an array entry, or a subroutine call."""
        if self.tokenizer.token in ");": return
        self.open_tag("term")
        token = self.tokenizer.token
        token_type = self.tokenizer.token_type
        if token_type == self.INT_CONSTANT:
            self.expect(self.INT_CONSTANT)
        elif token_type == self.STRING_CONSTANT:
            self.expect(self.STRING_CONSTANT)
        elif token in self.KEYWORD_CONSTANT:
            self.expect(self.KEYWORD)
        elif token_type == self.IDENTIFIER:
            self.expect(self.IDENTIFIER)
            if self.tokenizer.token == ".": # In case of subroutine call
                self.expect(".")
                self.expect(self.IDENTIFIER)
                self.expect("(")
                self.compile_expression_list()
                self.expect(")")
            elif self.tokenizer.token == "(":
                self.expect("(")
                self.compile_expression_list()
                self.expect(")")
            elif self.tokenizer.token == "[":
                self.expect("[")
                self.compile_expression()
                self.expect("]")
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
            raise Exception(
            "INVALID TOKEN: unexpected term element '{}'".format(token))
        self.close_tag("term")

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.open_tag("expressionList")
        self.compile_expression()
        while self.tokenizer.token == ",":
            self.expect(",")
            self.compile_expression()
        self.close_tag("expressionList")

    def expect(self, expected):
        """If token is valid, generates XML. Advances."""
        token = self.tokenizer.token
        token_type = self.tokenizer.token_type
        if type(expected) is tuple:
            if not token in expected:
                if token_type != self.IDENTIFIER:
                    raise Exception(
                        "INVALID TOKEN: expected {} or identifier"\
                        .format(expected))
        elif type(expected) is int:
            if token_type != expected:
                raise Exception(
                    "INVALID TOKEN: expected " + self.TAGS[token_type])
        elif token != expected:
            raise Exception(
                "INVALID TOKEN: expected '{}'".format(expected))
        elif token == None:
            return # End of File
        self.open_close_tag(self.TAGS[token_type], token)
        self.tokenizer.advance()
    
    def expect_special(self, token):
        """Generates XML without checking for validity. Advances."""
        token_type = self.tokenizer.token_type
        self.open_close_tag(self.TAGS[token_type], token)
        self.tokenizer.advance()

    def open_tag(self, tag_name):
        """Generates an open XML tag."""
        tag = "{0}<{1}>\n".format("  "*self.tab_level, tag_name)
        self.xml.append(tag)
        self.tab_level += 1
    
    def close_tag(self, tag_name):
        """Generates a close XML tag."""
        self.tab_level -= 1
        self.xml.append(
            "{0}</{1}>\n".format("  "*self.tab_level, tag_name))
    
    def open_close_tag(self, tag_name, value=" "):
        """Generates open and close XML tags on a single line."""
        if value != " ": value = " {} ".format(value)
        self.xml.append(
            "{0}<{1}>{2}</{1}>\n".format(
                "  "*self.tab_level, tag_name, value))