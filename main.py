from lexico.scanner import Scanner
from sintatico.parser import Parser
from sintatico.tradutor import Tradutor

if __name__ == '__main__':
    file_code_fonts = ['exemplos.md']

    for file_code_font in file_code_fonts: 
        # Lexical analysis
        scanner = Scanner(file_code_font)
        tokens, errors = scanner.analyse()

        # if errors:
        #     print(f"Lexical errors in {file_code_font}:")
        #     for error in errors:
        #         print(error)
        #     continue

        # Syntactic analysis
        parser = Parser(tokens)

        try:
            parser.program()
            print(f"Syntactic analysis for {file_code_font} completed successfully!")

            # Translation
            translator = Tradutor(tokens)
            python_code = translator.translate()

            print(f"Translation for {file_code_font}")
            print(python_code)

        except SyntaxError as e:
            print(f"\n=======\nSyntax error in {file_code_font}:\n{str(e)}")
