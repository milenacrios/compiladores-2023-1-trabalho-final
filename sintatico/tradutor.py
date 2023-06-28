from lexico.scanner import *


class Tradutor:
    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.token_index = 0
        self.current_token = None
        self.py_code = ""
        self.py_code_aux = ""

    def translate(self):
        self.py_code = ""
        self.current_token = self.get_next_token()
        self.program()
        return self.py_code

    def get_next_token(self):
        if self.token_index < len(self.list_tokens):
            self.current_token = self.list_tokens[self.token_index]
            self.token_index += 1
            return self.current_token
        else:
            return None

    def program(self):
        self.declaration()
        while self.current_token is not None:
            self.py_code +="\n"
            self.declaration()

    def declaration(self):
        if self.current_token[0] == 'keyword' and self.current_token[1] == 'fun':
            self.funDecl()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
            self.py_code += ""
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.consume('keyword', 'fun')
        self.py_code += "def "
        self.function()


    def function(self):
        if self.current_token[0] == 'identifier':
            
            identifier_ex = self.current_token[1] 
            #print('eh',colocar)
            self.consume('identifier')
            self.py_code += identifier_ex

   
        self.consume('delimiter', '(')
        self.py_code += "("
        
        self.parameters()
       # print('identifie', self.current_token[1])
       
        self.consume('delimiter', ')')
        self.py_code += ")"
        self.block()

    def parameters(self):
        parametro = self.current_token[1]
        self.py_code += parametro
        if self.current_token[0] == 'identifier':
            self.consume('identifier')
            print('oi')

        while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
            self.consume('delimiter')
            
            parametro = self.current_token[1]
            self.py_code += " , "
            self.py_code += parametro
            self.consume('identifier')
  

    def varDecl(self):
        self.consume('keyword', 'var')
        nome_variaveis = self.current_token[1]
        self.py_code += nome_variaveis
        self.consume('identifier')

        if self.current_token[0] == 'operator' and self.current_token[1] == '=':
            self.consume('operator', '=')
            self.py_code += " = "
            self.expression()
        self.consume('delimiter', ';')
        self.py_code +="\n"

    def statement(self):
        
        if self.current_token[0] == 'identifier':
            self.exprStmt()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'for':
            self.forStmt()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'if':
            self.ifStmt()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'print':
            self.printStmt()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'return':
            self.returnStmt()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'while':
            self.whileStmt()
        elif self.current_token[0] == 'delimiter' and self.current_token[1] == '{':
            self.block()

    def forStmt(self):
        self.consume('keyword', 'for')
        self.consume('delimiter', '(')
        if self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
            self.varDecl()
        elif self.current_token[0] == 'identifier':
            self.exprStmt()
        else:
            self.consume('delimiter', ';')
        if self.current_token[0] != 'delimiter' or self.current_token[1] != ')':
            self.expression()
        self.consume('delimiter', ';')
        if self.current_token[0] != 'delimiter' or self.current_token[1] != ')':
            self.expression()
        self.consume('delimiter', ')')
        self.statement()

    def ifStmt(self):
        self.consume('keyword', 'if')
        if self.py_code_aux != "elif":
            self.py_code += "if "
        self.consume('delimiter', '(')
        self.expression()
        self.consume('delimiter', ')')
        #self.py_code += ":\n\t"
        
        self.statement()
        if self.current_token[0] == 'keyword' and self.current_token[1] == 'else':
            self.consume('keyword', 'else')
            if self.current_token[0] == 'keyword' and self.current_token[1] == 'if':
                #print('aqui 2')
                self.py_code_aux = "elif"
                self.py_code += "\nelif "

                self.statement()
            else:
                #print('agora n ne ')
                self.py_code += "\nelse"
                self.statement()
        self.py_code_aux = " "

    def printStmt(self):
        self.consume('keyword', 'print')
        self.py_code += "print("
        self.expression()
        self.py_code += ")"
        self.consume('delimiter', ';')
        

    def returnStmt(self):
        self.consume('keyword', 'return')
        self.py_code += "return "
        if self.current_token[0] != 'delimiter' or self.current_token[1] != ';':
            self.expression()
        self.consume('delimiter', ';')

    def whileStmt(self):
        self.consume('keyword', 'while')
        self.py_code += "while "
        self.consume('delimiter', '(')
        self.expression()
        self.consume('delimiter', ')')
        self.statement()

    def block(self):
        self.consume('delimiter', '{')
        #print('aq')
        self.py_code += ":\n\t"
        while self.current_token[0] != 'delimiter' or self.current_token[1] != '}':
            self.declaration()
        self.consume('delimiter', '}')
        self.py_code += "\n"

    def exprStmt(self):
        self.expression()
        self.consume('delimiter', ';')

    def expression(self):
        self.assignment()

    def assignment(self):
        if self.current_token[0] == 'identifier':
            if self.current_token[1] == 'nil':
                self.py_code += "None"
            else:
                self.py_code += self.current_token[1]
            self.consume('identifier')
            if self.current_token[0] == 'operator' and self.current_token[1] == '=':
                self.py_code += " = "
                self.consume('operator', '=')
                self.assignment()
            else:
                self.logic_or()
        else:
            self.logic_or()

    def logic_or(self):
        self.logic_and()
        while self.current_token[0] == 'keyword' and self.current_token[1] == 'or':
            self.py_code += " or "
            self.consume('keyword', 'or')
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.current_token[0] == 'keyword' and self.current_token[1] == 'and':
            self.py_code += " and "
            self.consume('keyword', 'and')
            self.equality()

    def equality(self):
        self.comparison()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '!=' or self.current_token[1] == '=='):
            self.py_code += self.current_token[1]
            self.consume('operator')
            self.comparison()

    def comparison(self):
        self.term()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '>' or self.current_token[1] == '>=' or
                                                       self.current_token[1] == '<' or self.current_token[1] == '<='):
            self.py_code += " " + self.current_token[1] +  " "
            self.consume('operator')
            self.term()

    def term(self):
        self.factor()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '-' or self.current_token[1] == '+'):
            self.py_code += self.current_token[1]
            self.consume('operator')
            self.factor()

    def factor(self):
        self.unary()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '/' or self.current_token[1] == '*'):
            self.py_code += self.current_token[1]
            self.consume('operator')
            self.unary()

    def unary(self):
        if self.current_token[0] == 'operator' and (self.current_token[1] == '!' or self.current_token[1] == '-'):
            self.py_code += self.current_token[1]
            self.consume('operator')
            self.unary()
        else:
            self.call()

    def call(self):
        self.primary()
        while ((self.current_token[0] == 'delimiter' and self.current_token[1] == '(') or (
                self.current_token[0] == 'delimiter' and self.current_token[1] == '.')):
            if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
                self.consume('delimiter', '(')
                self.py_code += "("
                if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
                    self.arguments()
                self.consume('delimiter', ')')
                self.py_code += ")"
            elif self.current_token[0] == 'delimiter' and self.current_token[1] == '.':
                self.consume('delimiter', '.')
                self.consume('identifier')


        

    def primary(self):
        if self.current_token[0] == 'keyword' and (
                self.current_token[1] == 'true' or self.current_token[1] == 'false' or
                self.current_token[1] == 'nil' or self.current_token[1] == 'this'):
 
            self.py_code += self.current_token[1]
            
            self.consume('keyword')

        elif self.current_token[0] == 'integer':
            self.py_code += self.current_token[1]
            self.consume('integer')
        elif self.current_token[0] == 'string':
            self.py_code += self.current_token[1]
            self.consume('string')
        elif self.current_token[0] == 'identifier':
            self.py_code += self.current_token[1]
            self.consume('identifier')
        elif self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
            print('aqui deve add')
            self.py_code += "("
            self.consume('delimiter', '(')
            self.expression()
            if self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
                self.arguments()
            self.consume('delimiter', ')')
            self.py_code += ")"
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'super':
            self.consume('keyword', 'super')
            self.consume('operator', '.')
            self.consume('identifier')

    def arguments(self):
        self.expression()
        while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
            
            self.consume('delimiter', ',')
            self.py_code += " , "
            self.expression()

    def consume(self, token_type, expected_value=None):
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")

        if self.current_token[0] != token_type:
            raise SyntaxError(f" Expected {token_type} got {self.current_token[0]} \n ============\n Tokens:{self.list_tokens} \n =============\n current token:{self.current_token}")

        if expected_value and self.current_token[1] != expected_value:
            raise SyntaxError(f"Expected {expected_value} got {self.current_token[1]}")

        self.current_token = self.get_next_token() #if

    def translate(self):
        self.py_code = ""
        self.current_token = self.get_next_token()
        self.program()
        return self.py_code
