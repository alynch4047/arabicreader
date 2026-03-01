"""
Compile python code to javascript
"""

from byteplay import Code, Label

prog = \
"""
a = 2
b = 3
print a + b
"""

prog1 = \
"""
def add_it(a, b):
    return a + b
    
print add_it(1,2)
print add_it(4,5)
"""

compiled_code = compile(prog1, "pyjc", "exec" )

c = Code.from_code(compiled_code)
def output_code(code_obj, indent=""):
    for command, arg in code_obj.code:
        
        if type(arg) == Code:
            print indent, command, "__CODE__,"
            output_code(arg, indent=indent + " " * 4)
        elif type(arg) == Label:
            print dir(arg), repr(arg)
        else:
            print indent, command, str(arg) + ","
    print "__ENDCODE__ None,"
            
output_code(c)   

def output_js(compiled_code, js_code_str):
    pass

print output_js(c)         


