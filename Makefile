# Generació d'arxius ANTLR
make:
	java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -no-listener -visitor scheme.g4


clean:
	rm -f schemeLexer.py schemeParser.py schemeVisitor.py .interp.tokens
	rm -f *.interp
	rm -f *.tokens