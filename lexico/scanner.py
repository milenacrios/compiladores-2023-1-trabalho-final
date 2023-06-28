import re
from lexico.exceptions import *


class Scanner:
    def __init__(self, codigofont):
        with open(codigofont, 'r') as f:
            codigoFonte = f.read()
            self.codigoFonte = codigoFonte
            self.keywords = ['int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while',
                             'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return', 'main',
                             'printf', 'scanf', 'fun', 'and', 'or', 'true', 'false']
            self.types = [
                'int',
                'char',
                'long',
                'float',
                'double',
                'void',
                'String',
                'char'
            ]
    regex = {
        # Expressões regulares para palavras-chaves, identificadores, operadores, delimitadores, inteiros, floats e strings
        'keyword': r'(?<!\w)(int|true|false|or|and|fun|char|long|var|short|print|float|double|void|if|else|for|while|do|break|continue|struct|switch|case|default|return|main|printf|scanf|elif|auto|enum|extern|goto|register|signed|sizeof|static|typedef|union|unsigned|volatile|while)(?!\w)',
        'identifier': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
        'operator': r'(\+\+|--|->|&&|\|\||<<|>>|<=|>=|==|!=|[!%^&*+=\-\|/~<>\?])',
        'delimiter': r'(\(|\)|\[|\]|\{|\}|;|,|:)',
        'float': r'(?<!\w)[-+]?(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?\b',
        'integer': r'\d+[a-zA-Z]*',
        'string': r'"[^"\n]*"',
    }
    # r'(\*[_a-zA-Z][_a-zA-Z0-9]*)|([_a-zA-z][_a-zA-Z0-9]*)

    # r'(\*[_a-zA-Z][_a-zA-Z0-9]*)|([_a-zA-Z][_a-zA-Z0-9]*)'
    def analyse(self):
        #
        token_regex = '|'.join('(?P<%s>%s)' % (name, exp)
                               for name, exp in self.regex.items())
        regex_identificador = r'\b({})\b\s+([a-zA-Z_]\w*)'.format(
            '|'.join(self.keywords))

        tokens_list = []
        errors = []
        last_lexeme = None
        self.codigoFonte = re.sub(
            r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)', '', self.codigoFonte)
        for line in self.codigoFonte.split('\n'):
            for match in re.finditer(token_regex, line):
                for name, exp in self.regex.items():
                    if(match.lastgroup == name):
                        token_type = name
                        lexeme = match.group(name)
                        ###############################
                        try:
                            if token_type == 'keyword':
                                if lexeme in self.types and last_lexeme in self.types:
                                    print(
                                        "Identificador Inválido pois não pode ser uma palavra reservada")
                                else:
                                    if Keyword(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                    else:
                                        print("Error!")
                                        errors.append(
                                            'O lexeme {} não é válido'.format(lexeme))

                            elif token_type == 'identifier':
                                if Identifier(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'operator':
                                # if lexeme == '*' and (last_lexeme in self.types or last_lexeme in self.keywords or re.match(
                                #         self.regex['delimiter'], last_lexeme)):
                                #     token_type = 'pointer'
                                #     tokens_list.append((token_type, lexeme))
                                #     print(token_type)
                                # else:
                                    if Operator(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                    else:
                                        print("Error!")
                                        errors.append(
                                            'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'delimiter':
                                if Delimiter(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'integer':
                                if re.match(r'^\d+$', lexeme):
                                    if Integer(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                elif re.match(r"\d+\.\d+", lexeme):
                                    if Float(lexeme).validate():
                                        token_type = 'float'
                                        tokens_list.append(
                                            (token_type, lexeme))
                                else:
                                    token_type = 'identifier'
                                    print(token_type)
                                    print("Este é um identificador inválido")
                            elif token_type == 'float':
                                print(token_type)
                                if Float(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'string':
                                
                                if StringValidation(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                        except ExceptionGenerator as e:
                            print("Passou?")
                            print("Error: {}".format(e))
                            errors.append(
                                'O lexeme {} não é válido'.format(lexeme))
                        last_lexeme = lexeme

        return tokens_list, errors
