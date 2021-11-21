

class SymbolTable(dict):
  """
  TO DO
  """

  def __init__(self, scope):
    if scope == 'class':
      self.kind_count = {'STATIC': 0, 'FIELD': 0}
    elif scope == 'subroutine':
      self.kind_count = {'ARG': 0, 'VAR': 0}
    self.symbols = {}

  def define(self, name, type, kind):
    kind_idx = self.kind_count[kind]
    self.symbols[name] = (type, kind, kind_idx)
    self.kind_count[kind] += 1
    # To Do - handle errors
  
  def type_of(self, name):
    return self.symbols[name][0]

  def kind_of(self, name):
    return self.symbols[name][1]

  def index_of(self, name):
    return self.symbols[name][2]

  def kind_count_of(self, kind):
    return self.kind_count[kind]


# TEST
if __name__ == '__main__':
  st_class = SymbolTable('class')
  st_class.define("Point", "int", "STATIC")
  print(st_class.kind_count)
  print(st_class.symbols)
  print(st_class.kind_count)
  print(st_class.type_of('Point'))
  print(st_class.kind_of('Point'))
  print(st_class.index_of('Point'))
  print(st_class.symbols.get("asdf"))
  print(st_class.symbols.get("Point"))
  print()
  st_subroutine = SymbolTable('subroutine')
  st_subroutine.define("Thing", "char", "VAR")
  print(st_subroutine.kind_count)
  print(st_subroutine.symbols)
  print(st_subroutine.kind_count)
