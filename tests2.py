"""
Simple test script that runs JackCompiler and compares resulting .vm files (___Test.vm) to the .vm files provided by Nand to Tetris course (___.vm).
"""
from JackCompiler import JackCompiler


file_directories = [
  "assets2\Seven"
  # "assets2\ConvertToBin",
  # "assets2\Square",
  # "assets2\Average",
  # "assets2\Pong",
  # "assets2\ComplexArrays"
  ]

print("\nTEST OUTCOMES")
print("=============\n")

# test_count = 1
for program in file_directories:
  jc = JackCompiler(program, "Test")
  jc.analyze()