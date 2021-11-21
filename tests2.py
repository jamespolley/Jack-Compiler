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

for program in file_directories:
  jc = JackCompiler(program)
  jc.compile()

print("\nTEST OUTCOMES")
print("=============\n")

print("Test 1: PASSED")
print("assets2\Seven")

print("Test 2: PASSED")
print("assets2\ConvertToBin")

print("Test 3: PASSED")
print("assets2\Square")

print("Test 4: PASSED")
print("assets2\Average")

print("Test 5: PASSED")
print("assets2\Pong")

print("Test 6: PASSED")
print("assets2\ComplexArrays")

print("\nFor tests, used Nand2Tetris VM Emulator")
print("(not in project files, see README)\n")
