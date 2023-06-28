from lexico.scanner import *

class Parser: 
  def  __init__(self, list_tokens): 
    self.list_tokens = list_tokens #lista de tokens validados pelo analisador léxico
    self.token_index = 0 #primeiro índice da pilha
    self.current_token = None #token atual

  #ler token por token: 
  def  get_next_token(self): 
    if self.token_index < len(self.list_tokens): 
      self.current_token = self.list_tokens[self.token_index]
      self.token_index += 1
      print(f"\nToken Type: {self.current_token[0]}\nToken Value: {self.current_token[1]} \n \n ")
      return self.current_token
    else:
      return None
    
  def program(self): 
    self.current_token = self.get_next_token()
    while self.current_token is not None: 
      self.declaration()
            


  def declaration(self):                                                  
    if  self.current_token[0] == 'keyword' and self.current_token[1] == 'fun': #ok
      self.funDecl()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
      self.varDecl()
    else:
      self.statement()

  def funDecl(self): 
    self.consume('keyword', 'fun')
    self.function()

  def function(self):
    self.consume('identifier')
    self.consume('delimiter', '(')
    self.parameters()
    self.consume('delimiter', ')')
    self.block()
    
  def parameters(self): 
    if self.current_token[0] == 'identifier':
      self.consume('identifier')
    while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
      self.consume('delimiter', ',')
      self.consume('identifier')
      
  def varDecl(self): 
    self.consume('keyword', 'var')
    self.consume('identifier')
   
    if self.current_token[0] == 'operator' and self.current_token[1] == '=':
      self.consume('operator', '=')
      self.expression() 
    self.consume('delimiter', ';')
  
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
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      if self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
        self.varDecl()
      elif self.current_token[0] == 'identifier':
        self.exprStmt()
      else: 
        self.consume('delimiter', ';') 
      if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
        self.expression()
        self.consume('delimiter', ';')
        if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
          self.expression()
        self.consume('delimiter', ')')
      self.statement()

  def ifStmt(self): 
    self.consume('keyword', 'if')
    print("aaa")
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      self.expression()
      self.consume('delimiter', ')')
      self.statement()

      if self.current_token[0] == 'keyword' and self.current_token[1] == 'else':
        self.consume('keyword', 'else')
        self.statement()

  def printStmt(self): 
    self.consume('keyword', 'print')
    self.expression()
    self.consume('delimiter', ';')
  
  def returnStmt(self): 
    self.consume('keyword', 'return')
    if self.current_token[0] != 'delimiter' or self.current_token[1] != ';':
      self.expression()
    self.consume('delimiter', ';')

  def whileStmt(self): 
    self.consume('keyword', 'while')
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      self.expression()
      self.consume('delimiter', ')')
      self.statement()
      
  def block(self): 
    self.consume('delimiter', '{')
    while self.current_token[0] != 'delimiter' and self.current_token[1] != '}':
      self.declaration() 
    self.consume('delimiter', '}')

  def exprStmt(self): 
    self.expression() #depois precisa do ;
    self.consume('delimiter', ';')

  def expression(self): 
    self.assignment()
    
  def assignment(self): 
    if self.current_token[0] == 'identifier':
      self.consume('identifier')
      if self.current_token[0] == 'operator' and self.current_token[1] == '=':
        self.consume('operator', '=')
        self.assignment()
      else: 
        self.logic_or()
    else: 
      self.logic_or()
    
  def logic_or(self): 
    self.logic_and()
    while self.current_token[0] == 'keyword' and self.current_token[1] == 'or':
      self.consume('keyword', 'or')
      self.logic_and()
      
  def logic_and(self): 
    self.equality()
    while self.current_token[0] == 'keyword' and self.current_token[1] == 'and':
      self.consume('keyword', 'and')
      self.equality()
     
  def equality(self):
    self.comparison()
    while self.current_token[0] == 'operator' and (self.current_token[1] == '!=' or self.current_token[1] == '=='):
      self.consume('operator')
      self.comparison()

  def comparison(self): 
    self.term()
    while self.current_token[0] == 'operator' and (self.current_token[1] == '>' or self.current_token[1] == '>=' or
                                                       self.current_token[1] == '<' or self.current_token[1] == '<='):
      self.consume('operator')
      self.term()

  def term(self):
    self.factor()
    while self.current_token[0] == 'operator' and (self.current_token[1] == '-' or self.current_token[1] == '+'): 
      self.consume('operator')
      self.factor()

  def factor(self):
    self.unary()
    while self.current_token[0] == 'operator' and (self.current_token[1] == '/' or self.current_token[1] == '*'):
      self.consume('operator')
      self.unary()

  def unary(self):
    if self.current_token[0] == 'operator' and (self.current_token[1] == '!' or self.current_token[1] == '-'):
      self.consume('operator')
      self.unary()
    else:
      self.call()

  def call(self): 
    self.primary()
    while ((self.current_token[0] == 'delimiter' and self.current_token[1] == '(') or (self.current_token[0] == 'delimiter' and self.current_token[1] == '.')):
      if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
        self.consume('delimiter', '(')
        if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
          self.arguments()
          self.consume('delimiter', ')')
      elif self.current_token[0] == 'delimiter' and self.current_token[1] == '.':
        self.consume('delimiter', '.')
        self.consume('identifier')
    
          
  def primary(self): 
    if self.current_token[0] == 'keyword' and (self.current_token[1] == 'true' or self.current_token[1] == 'false' or
                                                   self.current_token[1] == 'nil' or self.current_token[1] == 'this'):
      self.consume('keyword')

    elif self.current_token[0] == 'integer':
      self.consume('integer')
    elif  self.current_token[0] == 'string':
      self.consume('string')
    elif self.current_token[0] == 'identifier':
      self.consume('identifier')
    elif self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      self.expression()
      if self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
        self.arguments()
      self.consume('delimiter', ')')
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'super':
      self.consume('keyword', 'super')
      self.consume('operator', '.')
      self.consume('identifier')

  def arguments(self):
    self.expression()
    while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
      self.consume('delimiter', ',')
      self.expression()                                      

  def consume(self, token_type, expected_value=None):
    if self.current_token is None:
      raise SyntaxError("Unexpected end of input")

    if self.current_token[0] != token_type:
      raise SyntaxError(f" Expected {token_type} got {self.current_token[0]} \n ============ \n \n")

    if expected_value is not None and self.current_token[1] != expected_value:
      raise SyntaxError(f" Expected {expected_value} got {self.current_token[1]} \n ============ \n\n")

    self.current_token = self.get_next_token()


        