from Tokenizer import Tokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
  """
  TO DO -----
  """

  KEYWORD = 0
  IDENTIFIER = 1
  SYMBOL = 2
  INT_CONSTANT = 3
  STRING_CONSTANT = 4

  OP = ("+", "-", "*", "/", "=", "&", "|", "<", ">")
  OP_TO_COMMAND = {
    '+': 'add'
    # TO DO - fill in
  }

  kind_to_segment = {
    'ARG': 'arg',
    'STATIC': 'static',
    'VAR': 'local',
    'FIELD': 'this'}

  def __init__(self, file):
    self.tokenizer = Tokenizer(file)
    self.vm_writer = VMWriter()
    self.current_class_name = None
    self.class_symbols = None
    self.subroutine_symbols = None
  
  def compile(self):
      """Compiles Jack code into VM code."""
      self.tokenizer.advance()
      while self.tokenizer.has_more_chars():
        self.compile_class()
      return self.vm_writer

  def compile_class(self):
    """Compiles a complete class."""
    t = self.tokenizer
    self.expect('class')
    t.advance()
    self.expect(self.IDENTIFIER)
    self.current_class_name = t.token
    t.advance()
    self.expect('{')
    t.advance()
    # self.compile_class_var_dec() --- to implement
    self.compile_subroutine_dec()
    print(self.vm_writer)
    print(t.token)
    self.expect('}')
    t.advance()
  
  def compile_class_var_dec(self):
    pass
  
  def compile_subroutine_dec(self):
    t = self.tokenizer
    while t.token in ('constructor', 'function', 'method'):
      self.subroutine_symbols = SymbolTable('subroutine')
      subroutine_type = t.token
      if subroutine_type == 'method':
        symbols.define('this', self.current_class_name, 'ARG')
      t.advance()
      t.advance()
      self.expect(self.IDENTIFIER)
      function_name = '{}.{}'.format(self.current_class_name, t.token)
      t.advance()
      t.advance()
      # self.compile_param_list() # to implement
      t.advance()
      t.advance()
      # self.compile_var_dec() # to implement
      n_args = self.subroutine_symbols.kind_count_of('VAR')
      self.vm_writer.write_function(function_name, n_args)
      if subroutine_type == 'constructor':
        n_fields = self.class_symbols.kind_count_of('FIELD')
        self.vm_writer.write_push('const', n_fields)
        self.vm_writer.write_call('Memory.alloc', 1)
        self.vm_writer.write_pop('pointer', 0)
      elif subroutine_type == 'method':
        self.vm_writer.write_push('arg', 0)
        self.generator.write_pop('pointer', 0)
      self.compile_statements()
      print(t.token)
      print('-----')
      t.advance()
      print(t.token)
      print('-----')
  
  def compile_param_list(self):
    pass

  def compile_subroutine_body(self):
    pass

  def compile_var_dec(self):
    pass

  def compile_statements(self):
    token = self.tokenizer.token
    if token == 'if': self.compile_if_statement()
    elif token == 'let': self.compile_let_statement()
    elif token == 'if': self.compile_if_statment()
    elif token == 'while': self.compile_while_statement()
    elif token == 'do': self.compile_do_statement()
    elif token == 'return': self.compile_return_statement()
    else: return
    self.compile_statements()

  def compile_let_statement(self):
    pass

  def compile_if_statement(self):
    pass

  def compile_while_statement(self):
    pass

  def compile_do_statement(self):
    print("----------")
    t = self.tokenizer
    t.advance()
    self.expect(self.IDENTIFIER)
    var_name = t.token
    t.advance()
    self.compile_subroutine_call(var_name)
    self.vm_writer.write_pop('temp', 0)
    t.advance()
    # pass

  def compile_return_statement(self):
    t = self.tokenizer
    t.advance() # expect return
    if t.token != ';':
      self.compile_expression()
    else:
      self.vm_writer.write_push('const', 0)
    self.vm_writer.write_return()
    t.advance() #expect ;

  def compile_subroutine_call(self, var_name):
    print(12345)
    t = self.tokenizer
    function_name = var_name
    n_args = 0

    if t.token == '.':
      t.advance()
      subroutine_name = t.token
      t.advance()
      # print(self.subroutine_symbols[var_name])
      # type, kind, kind_idx = self.subroutine_symbols[var_name]
      # ALSO ACCESS CLASS SYMBOLS?!!!
      if self.subroutine_symbols.get(var_name) != None:
        segment = self.kind_to_segment[self]
        self.vm_writer.write_push('push', segment, kind_idx)
        function_name = '{}.{}'.format(var_name, subroutine_name)
        n_args += 1
      else: function_name = '{}.{}'.format(var_name, subroutine_name)
    elif t.token == '(':
      subroutine_name = var_name
      function_name = '{}.{}'.format(self.current_class_name, subroutine_name)
      # n_args?????
      self.vm_writer.write_push('this', 0) # POINTER
    t.advance()
    self.compile_expression_list()
    # n_args???, expression list
    t.advance()
    n_args = 1 # hardcoded for now, test with Seven test class
    self.vm_writer.write_call(function_name, n_args)  

  def compile_expression_list(self):
    # To Do - return number of args (class variable or return value??)
    t = self.tokenizer
    while t.token != ')':
      t.advance() # expect ',' ???
      
      self.compile_expression()
    return

  def compile_expression(self):
    t = self.tokenizer
    self.compile_term()
    while t.token in self.OP:
      op = t.token
      t.advance()
      print(t.token)
      print(op)
      print('----------=====')
      self.compile_term()
      if op in '+': # fill out - TO DO
        print(self.OP_TO_COMMAND[op])
        self.vm_writer.write_arithmetic_logic(self.OP_TO_COMMAND[op])
      elif op == '*':
        self.vm_writer.write_call('Math.multiply', 2)
      elif op == '/':
        self.vm_writer.write_call('Math.divide', 2)
      else:
        # TO DO - error
        pass


  def compile_term(self):
    print('got here')
    t = self.tokenizer
    print(t.token)
    if t.token_type == self.INT_CONSTANT:
      self.vm_writer.write_push('const', int(t.token))
      t.advance()
    elif t.token == '(':
      t.advance()
      self.compile_expression()
      t.advance()

    # TO DO - handle other token types







  # compile expression, term, expression list?, 




  def expect(self, expected):
    token = self.tokenizer.token
    token_type = self.tokenizer.token_type
    if token == expected: return
    elif type(expected) is int:
      if token_type == expected: return
      raise Exception("TO IMPLEMENT")
    raise Exception(
      "INVALID TOKEN: expected '{}'".format(expected))
    

    
      
 