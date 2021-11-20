# TO DO - error handling??

class VMWriter(list):
  """
  TO DO
  """

  def __init__(self):
    pass
  
  def write_push(self, segment, index):
    """TO DO"""
    self.append('push {} {}'.format(segment, index))
  
  def write_pop(self, segment, index):
    """TO DO"""
    self.append('pop {} {}'.format(segment, index))
  
  def write_arithmetic_logic(self, command):
    """TO DO"""
    self.append(command)

  def write_label(self, label):
    """TO DO"""
    self.append('label ' + label)

  def write_goto(self, label):
    """TO DO"""
    self.append('goto ' + label)

  def write_if_goto(self, label):
    """TO DO"""
    self.append('if-goto ' + label)

  def write_call(self, name, n_args):
    """TO DO"""
    self.append('call {} {}'.format(name, n_args))

  def write_function(self, name, n_local_vars):
    """TO DO"""
    self.append('function {} {}'.format(name, n_local_vars))

  def write_return(self):
    """TO DO"""
    self.append('return')


# TESTS
w = VMWriter()
w.write_push('local', 99)
w.write_pop('local', 100)
w.write_arithmetic_logic('add')
w.write_label('Banana')
w.write_goto('Banana')
w.write_if_goto('Banana')
w.write_call('PeelBanana', 4)
w.write_function('PeelBanana', 4)
w.write_return()
print(w)