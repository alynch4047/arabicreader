

/*
 *Run a python program in javascript 
 */

var output_ = "";
var log_ = "";

function log(message) {
	log_ += message + '\n';
}

function output(message) {
	output_ += message;
}

function getProgram1() {
	/*
	 * """
a = 2
b = 3
print a + b
"""
	 */

	var l1 = ["SetLineno",  2];
	var l2 = ["LOAD_CONST",  2];
	var l3 = ["STORE_NAME",  "a"];
	var l4 = ["LOAD_CONST",  3];
	var l5 = ["STORE_NAME",  "b"];
	var l6 = ["LOAD_NAME",  "a"];
	var l7 = ["LOAD_NAME", "b"];
	var l8 = ["BINARY_ADD", null];
	var l9 = ["PRINT_ITEM", null];
	var l10 = ["PRINT_NEWLINE", null];
	var l11 = ["LOAD_CONST", null];
	var l12 = ["RETURN_VALUE", null];
	 
	var program = [l1, l2, l3, l4, l5, l6, l7, l8, l9,l10, l11, l12];
	return program;
}

function getProgram2() {
	/*
	 * """
def add_it(a, b):
    return a + b
    
print add_it(1,2)
print add_it(4,5)
"""
	 */
	prog_str = 
	 "SetLineno 2," +
	 "LOAD_CONST __CODE__," + 
	  "SetLineno 3, " +
	     "LOAD_FAST a," +
	     "LOAD_FAST b," +
	     "BINARY_ADD None," +
	     "RETURN_VALUE None," +
	     "__ENDCODE__ None," +
	 "MAKE_FUNCTION 0," +
	 "STORE_NAME add_it," +
	 "SetLineno 5," +
	 "LOAD_NAME add_it," +
	 "LOAD_CONST 1, " +
	 "LOAD_CONST 2, " +
	 "CALL_FUNCTION 2, " +
	 "PRINT_ITEM None, " +
	 "PRINT_NEWLINE None, " +
	 "SetLineno 6, " +
	 "LOAD_NAME add_it," +
	 "LOAD_CONST 4," +
	 "LOAD_CONST 5," +
	 "CALL_FUNCTION 2," +
	 "PRINT_ITEM None," +
	 "PRINT_NEWLINE None," +
	 "LOAD_CONST None," +
	 "RETURN_VALUE None," +
	 "__ENDCODE__ None,"
	 prog_joined = prog_str.split(",");
	 prog = [];
	 for each (var line in prog_joined) {
		 line = line.trim();
		 line_parts = line.split(" ");
		 if (line_parts.length == 2) {
			 prog.push([line_parts[0], line_parts[1]]);
		 }
	 }
	 for each (var line in prog) {
		 print('line: ' + line + '\n');
	 }
	 return prog;
}

function setLineNo(frame, arg) {
}

function loadConst(frame, arg) {
	frame.stack.push(arg);
}

function storeName(frame, arg) {
	frame.local_variables[arg] = frame.stack.pop();
}

function loadName(frame, arg) {
	frame.stack.push(frame.local_variables[arg])
}

function binaryAdd(frame, arg) {
	frame.stack.push(frame.stack.pop() + frame.stack.pop());
}

function printItem(frame, arg) {
	output(frame.stack[frame.stack.length - 1]);
}

function printNewLine(frame, arg) {
	output('\n');
}


var processors = {"SetLineno": setLineNo,
		"LOAD_CONST": loadConst,
		"STORE_NAME": storeName,
		"LOAD_NAME": loadName,
		"BINARY_ADD": binaryAdd,
		"PRINT_ITEM": printItem,
		"PRINT_NEWLINE": printNewLine
};

function read_func(prog, ix) {
	code = [];
	for(var ix2 = ix; ix2 < prog.length; ix2++) {
		var line = prog[ix];
		var command = line[0];
		var arg = line[1];
		if (command == "__ENDCODE__") {
			break;
		}
		else {
			code.push([line[0], line[1]]);
		}
	}
	return {func: code, ix: ix2};
}

function run(prog) {
	var frame = {
		local_variables: {},
		stack: []
	};
	var return_value = null;
	for(var ix = 0; ix < prog.length; ix++) {
		var line = prog[ix];
		var command = line[0];
		var arg = line[1];
		
		if (arg == "__CODE__") {
			var ret = read_func(prog, ix);
			var func = ret.func;
			ix = ret.ix;
			loadConst(frame, func);
			continue;
		}
		
		else if (command == "RETURN_VALUE") {
			return_value = frame.stack[frame.stack.length - 1]; 
			break;
		}
		else {
			var processor_func = processors[command];
			log("call command " + command);
			processor_func(frame, arg);
		}

	}
	return return_value;
}


function test1() {
	var prog = getProgram1();
	output_ = "";
	log_ = "";
	val = run(prog);
	if (output_ != "5\n") {
		print("fail: " + val);
		print("LOG:\n" + log_);
		print("OUTPUT:\n" + output_);
	}
	else print("pass");

}

function test2() {
	var prog = getProgram2();
	output_ = "";
	log_ = "";
	val = run(prog);
	if (output_ != "3\n9") print("fail: " + val); else print("pass");
	print("LOG:\n" + log_);
	print("OUTPUT:\n" + output_);
}

test1()
test2()
