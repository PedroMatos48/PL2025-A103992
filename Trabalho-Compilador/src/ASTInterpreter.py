from PascalYacc import parser
from test import ex1, ex2, ex3, ex4, ex5, ex6,ex7, ex8, ex9, ex10
from dataclasses import dataclass

@dataclass
class VarInfo:
    tipo: object
    position: int
    size: int = 1
    begin: int = 0
    isArray: bool = False
    const: bool = False
    value: object = 0

class ASTInterpreter:
    def __init__(self):
        self.symbols = {}
        self.vars = {}
        self.result = []
        self.current_line = 1 
        self.pos = 0

    def run(self):
        print("\nResultado:")
        for line in self.result:
            print(line)

    def interpret(self, node):
        node = node[1] 
        if node[0] == "MAIN":
            self._handle_commands(node[1])  # consts
            if node[1]:
                self.current_line += 1
            
            self._handle_commands(node[2])  # vars
            if node[2]:
                self.current_line += 1
            self.current_line += 1

            self.result.append("START:")
            self._handle_commands(node[3])  # statements
            self.current_line += 1
            self.result.append("STOP")
        else:
            raise Exception(f"Expected 'MAIN' node, got {node[0]}")

    def _handle_commands(self, node):
        if isinstance(node, list):
            for stmt in node:
                self._handle_commands(stmt)
            return

        while isinstance(node, tuple) and len(node) == 1 and isinstance(node[0], tuple):
            node = node[0]

        cmd = node[0]
        self.current_line += 1        

        if cmd == "CONST":
            self._handle_const(node)
        elif cmd == "VARS":
            self._handle_vars(node)
        elif cmd == "STATEMENT_LIST":
            self.current_line +=1
            for statement in node[1]:
                self._handle_commands(statement)
        elif cmd == "IF":
            self._handle_if(node)
        elif cmd == "READ":
            self._handle_read(node)
        elif cmd == "READLN":
            self._handle_readln(node)
        elif cmd == "WRITE":
            self._handle_write(node)
        elif cmd == "WRITELN":
            self._handle_writeln(node)
        elif cmd == "ASSIGN":
            self._handle_assign(node)
        elif cmd == "WHILE":
            self._handle_while(node)
        elif cmd == "FOR":
            self._handle_for(node)
        elif cmd == "FOR_D":
            self._handle_for_downto(node)
        else:
            raise Exception(f"Unknown command {cmd} at line {self.current_line}")

    def _handle_const(self, node):
        for const in node[1]:
            value = const[1]
            name = const[0]
            self.current_line+=1
            if name in self.vars:
                raise Exception(f"Constant '{name}' already declared at line {self.current_line}")
            if isinstance(value, str):
                if value in self.vars and not self.vars[value].const:
                    raise Exception(f"Cannot assign variable '{value}' to constant '{name}' at line {self.current_line}")
                if value.isdigit():
                    self.vars[name]= VarInfo("integer", self.pos, 1, 0, False, True, value)
                elif "." in value and all(part.isdigit() for part in value.split(".")):
                    self.vars[name]= VarInfo("float", self.pos, 1, 0, False, True, value)
                elif value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    self.vars[name]= VarInfo("string", self.pos, 1, 0, False, True, value)
                elif value == "true" or value == "false":
                    self.vars[name]= VarInfo("boolean", self.pos, 1, 0, False, True, value) 
                else:
                    raise Exception(f"Unrecognized constant value '{value}' at line {self.current_line}")

    def _handle_vars(self, node):
        valid_types = {"integer", "boolean", "real", "string", "char"}

        for vars_group in node[1]:
            tipo = vars_group[0]
            self.current_line+=1
            for var in vars_group[1]:
                if var in self.vars:
                    raise Exception(f"Variable '{var}' already declared at line {self.current_line}")

                # ARRAY: ("ARRAY", start_idx, end_idx, base_type)
                if isinstance(tipo, tuple) and tipo[0] == "ARRAY":
                    start_tok, end_tok, base_type = tipo[1], tipo[2], tipo[3]

                    if isinstance(start_tok, str) and not start_tok.isdigit():
                        if start_tok not in self.vars or not self.vars[start_tok].const:
                            raise Exception(f"Array bound '{start_tok}' must be a declared constant at line {self.current_line}")
                        if self.vars[start_tok].tipo != "integer":
                            raise Exception(f"Array bound '{start_tok}' must be of type integer at line {self.current_line}")
                        start_idx = int(self.vars[start_tok].value)
                    else:
                        start_idx = int(start_tok)

                    if isinstance(end_tok, str) and not end_tok.isdigit():
                        if end_tok not in self.vars or not self.vars[end_tok].const:
                            raise Exception(f"Array bound '{end_tok}' must be a declared constant at line {self.current_line}")
                        if self.vars[end_tok].tipo != "integer":
                            raise Exception(f"Array bound '{end_tok}' must be of type integer at line {self.current_line}")
                        end_idx = int(self.vars[end_tok].value)
                    else:
                        end_idx = int(end_tok)

                    if start_idx > end_idx:
                        raise Exception(f"Invalid array bounds: {start_idx} to {end_idx} at line {self.current_line}")

                    if base_type.lower() not in valid_types:
                        raise Exception(f"Invalid array base type '{base_type}' for variable '{var}' at line {self.current_line}")

                    size = end_idx - start_idx + 1
                    self.vars[var] = VarInfo(base_type, self.pos, size, start_idx, isArray=True)
                    self.result.append(f"PUSHI {size}")
                    self.result.append("ALLOCN")

                elif tipo == "string":
                    size = 256
                    self.vars[var] = VarInfo(tipo, self.pos, size, 1, isArray=True)
                    self.result.append(f"PUSHS \"\"")

                else:
                    if tipo.lower() not in valid_types:
                        raise Exception(f"Invalid type '{tipo}' for variable '{var}' at line {self.current_line}")

                    self.vars[var] = VarInfo(tipo, self.pos)
                    init = "PUSHI 0" if tipo.lower() in ("integer", "boolean") else 'PUSHS ""'
                    self.result.append(init)

                self.pos += 1

    def _handle_assign(self, node):
        _, target, expr = node
        self.valid_assign(target,expr)

        self._eval_expr(expr,False)
        if isinstance(target, tuple):
            array_name, index_expr = target
            self.valid_assign(array_name,expr)
            if array_name not in self.vars:
                raise Exception(f"Array '{array_name}' not declared at line {self.current_line}")
            
            if self.vars[array_name].const:
                raise Exception(f"Cannot assign to constant array '{array_name}' at line {self.current_line}")
            
            self.result.append(f"PUSHG {self.get_var_index(array_name)}")
            self.valid_index(array_name, index_expr)
            
            self._eval_expr(index_expr)
            self.result.append(f"PUSHI {self.getSum(array_name)}")
            self.result.append(f"ADD")
            self._eval_expr(expr)

            self.result.append("STOREN")
        else:
            if target not in self.vars:
                raise Exception(f"Variable '{target}' not declared at line {self.current_line}")
            
            if self.vars[target].const:
                raise Exception(f"Cannot assign to constant '{target}' at line {self.current_line}")
            
            self.result.append(f"STOREG {self.get_var_index(target)}")

    def _eval_expr(self, expr, charCode=True):
        if isinstance(expr, str):
            if expr.startswith(("'", '"')) and expr.endswith(("'", '"')):
                clean_expr = expr[1:-1]
                self.result.append(f'PUSHS "{clean_expr}"')
                if charCode:
                    if len(clean_expr)==1:
                        self.result.append("CHRCODE")
            elif expr.isdigit():
                self.result.append(f"PUSHI {int(expr)}")
            elif expr.lower() == 'true':
                self.result.append("PUSHI 1")
            elif expr.lower() == 'false':
                self.result.append("PUSHI 0")
            elif "." in expr and all(part.isdigit() for part in expr.split(".")):
                self.result.append(f"PUSHF {float(expr)}")
            elif expr == "":
                self.result.append(f"PUSHS \"\"")
            else:
                v = self.vars[expr]
                if v.const:
                    self.push_const(expr)
                else:
                    self.result.append(f"PUSHG {self.get_var_index(expr)}")

        elif isinstance(expr, tuple):
            if len(expr) == 2 and isinstance(expr[0], str):
                array_name, index_expr = expr
                if array_name in self.vars and self.vars[array_name].tipo == "string":
                    self.result.append(f"PUSHG {self.get_var_index(array_name)}")
                    self._eval_expr(index_expr)
                    self.result.append("PUSHI -1")
                    self.result.append("ADD")
                    self.result.append("CHARAT")
                    return
                elif array_name in self.vars and self.vars[array_name].isArray:
                    self.result.append(f"PUSHG {self.get_var_index(array_name)}")
                    self.valid_index(array_name, index_expr)
                    self._eval_expr(index_expr)
                    self.result.append(f"PUSHI {self.getSum(array_name)}")
                    self.result.append(f"ADD")
                    self.result.append("LOADN")
                    return
            op = expr[0].upper() if isinstance(expr[0], str) else expr[0]
            if op == 'VAR':
                varname = expr[1]
                v = self.vars[varname]
                if v.const:
                    self.push_const(varname)
                else:
                    self.result.append(f"PUSHG {self.get_var_index(varname)}")
                return
            if op == "STRING":
                val = expr[1]
                self.result.append(f'PUSHS "{val}"')
                return
            if op in ('ADD', 'SUB', 'MUL', 'RDIV', 'DIV', 'MOD',
                      '=', '<>', '<', '>', '<=', '>=',
                      'AND', 'OR'):     
                self.valid_assign(expr[1],expr[2])

                self._eval_expr(expr[1])
                self._eval_expr(expr[2])
                self._handle_operation(expr)
            elif op == 'NOT':
                self._eval_expr(expr[1])
                self.result.append("NOT")
            elif op == 'LENGTH':
                self._eval_expr(expr[1])
                self.result.append("STRLEN")
            else:
                raise Exception(f"Unknown operation in expression: {op}")

    def _handle_operation(self, node):
        op = node[0].upper()
        ops = {
            'ADD': 'ADD', 'SUB': 'SUB', 'MUL': 'MUL',
            'RDIV': 'DIV', 'DIV': 'DIV', 'MOD': 'MOD',
            '=': 'EQUAL', '<>': 'DIFF',
            '<': 'INF', '>': 'SUP',
            '<=': 'INFEQ', '>=': 'SUPEQ',
            'AND': 'AND', 'OR': 'OR'
        }
        opcode = ops.get(op)
        if opcode is None:
            raise Exception(f"Unknown operator {op}")
        self.result.append(opcode)

    def _handle_if(self, node):
        cond = node[1]
        then_block = node[2]
        else_block = None

        if len(node) > 4 and node[3] == "ELSE":
            else_block = node[4]
        elif len(node) == 4:
            else_block = node[3]

        label_else = f"L{self.current_line}ELSE"
        label_end = f"L{self.current_line}END"

        self._eval_expr(cond)
        self.result.append(f"JZ {label_else}")

        if isinstance(then_block, list):
            for stmt in then_block:
                self._handle_commands(stmt)
        else:
            self._handle_commands(then_block)

        self.result.append(f"JUMP {label_end}")
        self.result.append(f"{label_else}:")

        if else_block:
            if isinstance(else_block, list):
                for stmt in else_block:
                    self._handle_commands(stmt)
            else:
                self._handle_commands(else_block)

        self.result.append(f"{label_end}:")

    def _handle_while(self, node):
        _, cond, body = node
        start_label = f"L{self.current_line}START"
        end_label = f"L{self.current_line}END"

        self.result.append(f"{start_label}:")
        self._eval_expr(cond)
        self.result.append(f"JZ {end_label}")

        self._handle_commands(body)

        self.result.append(f"JUMP {start_label}")
        self.result.append(f"{end_label}:")

    def _handle_for(self, node):
        _, var, start, end, body = node

        self._eval_expr(start)
        self.result.append(f"STOREG {self.get_var_index(var)}")

        start_label = f"L{self.current_line}FOR"
        end_label = f"L{self.current_line}ENDFOR"

        self.result.append(f"{start_label}:")

        self.result.append(f"PUSHG {self.get_var_index(var)}")
        self._eval_expr(end)
        self.result.append("INFEQ")
        self.result.append(f"JZ {end_label}")

        if isinstance(body, list):
            for stmt in body:
                self._handle_commands(stmt)
        else:
            self._handle_commands(body)

        self.result.append(f"PUSHG {self.get_var_index(var)}")
        self.result.append("PUSHI 1")
        self.result.append("ADD")
        self.result.append(f"STOREG {self.get_var_index(var)}")

        self.result.append(f"JUMP {start_label}")
        self.result.append(f"{end_label}:")

    def _handle_for_downto(self, node):
        _, var, start, end, body = node

        self._eval_expr(start)
        self.result.append(f"STOREG {self.get_var_index(var)}")

        start_label = f"L{self.current_line}FOR"
        end_label = f"L{self.current_line}ENDFOR"

        self.result.append(f"{start_label}:")

        self.result.append(f"PUSHG {self.get_var_index(var)}")
        self._eval_expr(end)
        self.result.append("SUPEQ")
        self.result.append(f"JZ {end_label}")

        if isinstance(body, list):
            for stmt in body:
                self._handle_commands(stmt)
        else:
            self._handle_commands(body)

        self.result.append(f"PUSHG {self.get_var_index(var)}")
        self.result.append("PUSHI 1")
        self.result.append("SUB")
        self.result.append(f"STOREG {self.get_var_index(var)}")

        self.result.append(f"JUMP {start_label}")
        self.result.append(f"{end_label}:")

    def _handle_read(self, node):
        _, var = node
        if isinstance(var, tuple) and len(var) == 2:
            array_name, index_expr = var
            
            self.result.append(f"PUSHG {self.get_var_index(array_name)}")
            self.valid_index(array_name, index_expr)
            self._eval_expr(index_expr)
            self.result.append(f"PUSHI {self.getSum(array_name)}")
            self.result.append(f"ADD")
            
            self.result.append("READ")
            variable = self.vars[array_name]
            if variable.tipo.lower() == "integer":
                self.result.append("ATOI")
            elif variable.tipo.lower() == "real":
                self.result.append("ATOF")
            
            self.result.append("STOREN")
        else:        
            self.result.append("READ")
            variable = self.vars[var]
            if variable.tipo.lower() == "integer":
                self.result.append("ATOI")
            elif variable.tipo.lower() == "real":
                self.result.append("ATOF")
            self.result.append(f"STOREG {self.get_var_index(var)}")

    def _handle_readln(self, node):
        _, var = node
        
        if isinstance(var, tuple) and len(var) == 2:
            array_name, index_expr = var
            
            self.result.append(f"PUSHG {self.get_var_index(array_name)}")
            self.valid_index(array_name, index_expr)
            
            self._eval_expr(index_expr)
            self.result.append(f"PUSHI {self.getSum(array_name)}")
            self.result.append(f"ADD")
            
            self.result.append("READ")
            #self.result.append("WRITELN")
            variable = self.vars[array_name]
            if variable.tipo.lower() == "integer":
                self.result.append("ATOI")
            elif variable.tipo.lower() == "real":
                self.result.append("ATOF")
            
            self.result.append("STOREN")
        else:        
            self.result.append("READ")
            #self.result.append("WRITELN")
            if var == None:
                return
            variable = self.vars[var]
            if variable.tipo.lower() == "integer":
                self.result.append("ATOI")
            elif variable.tipo.lower() == "real":
                self.result.append("ATOF")
            self.result.append(f"STOREG {self.get_var_index(var)}")

    def _handle_write(self, node):
        _, values = node
        for kind, value in values:
            if kind == 'STRING':
                self.result.append(f'PUSHS "{value}"')
                self.result.append('WRITES')
            elif kind == 'VAR':
                if isinstance(value, tuple):
                    name, index = value
                    self.valid_index(name, index)
                    self.result.append(f'PUSHG {self.get_var_index(name)}')
                    self._eval_expr(index)
                    
                    var_type = self.vars[name].tipo.lower()
                    if var_type == "string":
                        self.result.append("PUSHI 1")
                        self.result.append("SUB")
                        self.result.append("CHARAT")
                        self.result.append("WRITECHR")
                        continue
                        
                    self.result.append(f"PUSHI {self.getSum(name)}")
                    self.result.append(f"ADD")
                    self.result.append(f'LOADN')
                    
                    if var_type in ('float', 'real'):
                        self.result.append('WRITEF')
                    elif var_type == 'integer':
                        self.result.append('WRITEI')
                    else:
                        raise Exception(f"Unsupported variable type'{var_type}' at line {self.current_line}")
                else:
                    index = self.get_var_index(value)
                    if self.vars[value].const:
                        self.push_const(value)
                        return
                    self.result.append(f'PUSHG {index}')
                    var_type = self.vars[value].tipo.lower()
                    if var_type in ('float', 'real'):
                        self.result.append('WRITEF')
                    elif var_type == "integer":
                        self.result.append('WRITEI')
                    else:
                        self.result.append("WRITES")
        
    def _handle_writeln(self, node):
        _, values = node

        for kind, value in values:
            if kind == 'STRING':
                self.result.append(f'PUSHS "{value}"')
                self.result.append('WRITES')
            elif kind == 'VAR':
                if isinstance(value, tuple):
                    name, index = value
                    if name not in self.vars:
                        raise Exception(f"Variable '{name}' not declared at line {self.current_line}")
                    self.valid_index(name, index)
                    self.result.append(f'PUSHG {self.get_var_index(name)}')
                    self._eval_expr(index)
                    
                    var_type = self.vars[name].tipo.lower()
                    if var_type == "string":
                        self.result.append("PUSHI 1")
                        self.result.append("SUB")
                        self.result.append("CHARAT")
                        self.result.append("WRITECHR")
                        continue
                        
                    self.result.append(f"PUSHI {self.getSum(name)}")
                    self.result.append(f"ADD")
                    self.result.append(f'LOADN')
                    
                    if var_type in ('float', 'real'):
                        self.result.append('WRITEF')
                    elif var_type == 'integer':
                        self.result.append('WRITEI')
                    else:
                        raise Exception(f"Unsupported variable type '{var_type}' at line {self.current_line}")
                else:
                    if value not in self.vars:
                        raise Exception(f"Undeclared variable '{value}' at line {self.current_line}")
                    if self.vars[value].const:
                        self.push_const(value)
                        return
                    index = self.get_var_index(value)
                    self.result.append(f'PUSHG {index}')
                    var_type = self.vars[value].tipo.lower()
                    if var_type in ('float', 'real'):
                        self.result.append('WRITEF')
                    elif var_type == "integer":
                        self.result.append('WRITEI')
                    else:
                        self.result.append("WRITES")
        self.result.append('WRITELN') 

    def get_var_index(self, varname):
        if self.vars[varname].const:
            raise Exception(f"Variable {varname} is constant at line {self.current_line}")
        elif varname in self.vars:
            return self.vars[varname].position
        else:
            raise Exception(f"Undeclared variable '{varname}' at line {self.current_line}")
        
    def getSum(self, name):
        var = self.vars[name]
        return 0 - var.begin

    def push_const(self, name):
        v = self.vars[name]
        if v.tipo.lower() == "integer":
            self.result.append(f"PUSHI {v.value}")
        elif v.tipo.lower() == "real":
            self.result.append(f"PUSHR {v.value}")
        elif v.tipo.lower() == "string":
            self.result.append(f"PUSHS {v.value}")
        elif v.tipo.lower() == "boolean":
            r = 0
            if v.value == True:
                r = 1
            self.result.append(f"PUSHI {r}")
        else:
            raise Exception(f"Invalid type '{v.tipo.lower}' at {self.current_line}")
    
    def valid_index(self, name, index):
        if isinstance(index, str) and index.isdigit():
            v = self.vars[name]
            if v.tipo.lower() != "string" and not index in range(v.begin, v.begin + v.size):
                raise Exception(f"Array {name} out of bounds at line {self.current_line}")
            
    def valid_assign(self, expr1, expr2):
        if isinstance(expr1, str) and isinstance(expr2, str):
            if (expr1.startswith(("'", '"')) and expr1.endswith(("'", '"')) or
                (expr1 in self.vars and self.vars[expr1].tipo.lower() in ["char", "string"])):
                if (expr2.startswith(("'", '"')) and expr2.endswith(("'", '"')) or
                    (expr2 in self.vars and self.vars[expr2].tipo.lower() in ["char", "string"])):
                    return

            if (expr1.isdigit() or
                (expr1 in self.vars and self.vars[expr1].tipo.lower() == "integer")):
                if (expr2.isdigit() or
                    (expr2 in self.vars and self.vars[expr2].tipo.lower() == "integer")):
                    return

            if (expr1.lower() in ('true', 'false') or
                (expr1 in self.vars and self.vars[expr1].tipo.lower() == "boolean")):
                if (expr2.lower() in ('true', 'false') or
                    (expr2 in self.vars and self.vars[expr2].tipo.lower() == "boolean")):
                    return

            if (self._is_float(expr1) or
                (expr1 in self.vars and self.vars[expr1].tipo.lower() == "real")):
                if (self._is_float(expr2) or
                    (expr2 in self.vars and self.vars[expr2].tipo.lower() == "real")):
                    return

            if expr1 in self.vars and expr2 in self.vars:
                if self.vars[expr1].tipo.lower() == self.vars[expr2].tipo.lower():
                    return

            raise Exception(f"Mismatched types for {expr1} and {expr2} at line {self.current_line}")

    def _is_float(self, value):
        try:
            float(value)
            return '.' in value
        except ValueError:
            return False

if __name__ == "__main__":
    ast = parser.parse(ex6)
    interp = ASTInterpreter()
    interp.interpret(ast)
    interp.run()