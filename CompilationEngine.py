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

  def __init__(self, file):
    self.tokenizer = Tokenizer(file)
    self.vm_writer = VMWriter()
    # self.vm = []
    self.current_class_name = None
    self.class_symbols = None
    self.subroutine_symbols = None
  
  def compile(self):
      """Compiles Jack code into VM code."""
      self.tokenizer.advance()
      while self.tokenizer.has_more_chars():
          self.compile_class()

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
    self.expect('}')
    t.advance()
  
  def compile_class_var_dec(self):
    pass
  
  def compile_subroutine_dec(self):
    t = self.tokenizer
    self.subroutine_symbols = SymbolTable('subroutine')
    subroutine_type = t.token
    if subroutine_type == 'method':
      symbols.define('this', self.current_class_name, 'ARG')
    t.advance()
    print(t.token)
    t.advance()
    print(t.token)
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
    t.advance()
  
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

  

  # compile while, do, return, expression, term, expression list?, 




  def expect(self, expected):
    token = self.tokenizer.token
    token_type = self.tokenizer.token_type
    if token == expected: return
    elif type(expected) is int:
      if token_type == expected: return
      raise Exception("TO IMPLEMENT")     
    raise Exception(
      "INVALID TOKEN: expected '{}'".format(expected))
    
      
 