import sys
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import *
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from visitor import SchemeVisitor


#Faig subclass del ErrorListener per tractar tots els errors sintàctics
class InterpretErrorListener(ErrorListener):
    def __init__(self):
        super(InterpretErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception()


def main(argv):
    # Agafar input i inicialització de classes ANTLR
    input_file = FileStream(argv[1], encoding="utf-8")
    lexer = schemeLexer(input_file)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)

    parser.removeErrorListeners()
    parser.addErrorListener(InterpretErrorListener)

    # Creem l'AST i el recorrem
    try:
        tree = parser.program()
    except Exception as e:
        print("Error de sintaxi")
        sys.exit(1)
    interpreter = SchemeVisitor()
    interpreter.visit(tree)

    # Trucada al main del programa Scheme
    if "main" not in interpreter.entorn:
        raise Exception("'main' not defined.")
    main_func = interpreter.entorn["main"]
    if "params" in main_func and len(main_func["params"]) > 0:
        raise Exception("'main' must not take any parameters.")
    interpreter.aplica_func(main_func["body"], {})


if __name__ == "__main__":
    main(sys.argv)
