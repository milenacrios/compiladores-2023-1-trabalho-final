import re


class ExceptionGenerator(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IdentifierException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Identifier:

    def __init__(self, value):
        self.value = value

    def validate(self):
        reserved_words = ['int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while',
                          'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return', 'main',
                          'printf', 'scanf', 'fun', 'or', 'and', 'true', 'false']
        if self.value in reserved_words:
            raise IdentifierException(
                f"Identificador Inválido: {self.value}")
        if not re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', self.value):
            raise IdentifierException(
                f"Identificador inválido: {self.value}.")

        return True


class KeywordException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Keyword:

    def __init__(self, value):
        self.value = value

    def validate(self): 
        # keyword_list = ['int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while',
        #                 'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return', 'main',
        #                 'printf', 'scanf']
        # if self.value not in keyword_list: 
        #     # print('entra aqui')
        #     raise KeywordException(
        #         f"Palavra reservada inválida: {self.value}")
        if not re.match(r'(?<!\w)(int|true|false|or|and|fun|char|long|short|float|var|double|print|void|if|else|for|while|do|break|continue|struct|switch|case|default|return|main|printf|scanf|elif|auto|enum|extern|goto|register|signed|sizeof|static|typedef|union|unsigned|volatile|while)(?!\w)', self.value):
            raise KeywordException(
                'Essa é uma palavra reservada inválida: {}'.format(self.value))
        return True


class IntegerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Integer:
    def __init__(self, value):
        self.value = value

    def validate(self):
        if not re.match(r'\d+', self.value):
            raise IntegerException(
                'Este é um Int inválido: {}.'.format(self.value))
        return True


class FloatException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Float:
    SUPPORTED_TYPES = ['FLOAT']

    def __init__(self, value):
        self.value = value

    def validate(self):
        if not re.match(r'(?<!\w)[-+]?(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?\b', self.value):
            raise IntegerException(
                'Este é um Float inválido: {}.'.format(self.value))
        return True


class OperatorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Operator:
    SUPPORTED_TYPES = ['OPERATOR']

    def __init__(self, value):
        self.value = value

    def validate(self):
        if self.value not in [
            '++',
            '--',
            '=',
            '+',
            '-',
            '*',
            '/',
            '%',
            '==',
            '!=',
            '+=',
            '++',
            '<',
            '>',
            '<=',
            '>=',
            '!',
            '&&',
            '||',
                '&', '->']:
            raise OperatorException(
                'Este é um Operador inválido: {}.'.format(self.value))
        return True


class DelimiterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Delimiter:
    def __init__(self, value):
        self.value = value

    def validate(self):
        if not re.match(r'(\(|\)|\[|\]|\{|\}|;|,|:)', self.value):
            raise DelimiterException(
                'Este é um Delimitador inválido: {}.'.format(self.value))
        return self.value


class StringException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StringValidation:
    def __init__(self, value):
        self.value = value

    def validate(self):
        if not re.match(r'"[^"\n]*"', self.value):
            raise StringException(
                'Essa é uma String Inválida: {}'.format(self.value))
        return self.value
