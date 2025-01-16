from schemeVisitor import schemeVisitor


# Visitors de tota la gràmatica
class SchemeVisitor(schemeVisitor):
    def __init__(self):
        self.entorn = (
            {}
        )  # Per guardar els identificadors de les constants i funcions definides

    # Visitor principal, examina tots els defines
    def visitProgram(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)

    def visitFunctiondef(self, ctx):
        func_name = ctx.IDENTIFIER(0).getText()
        parameters = [param.getText() for param in ctx.IDENTIFIER()[1:]]
        body = ctx.expression()
        self.entorn[func_name] = {
            "params": parameters,
            "body": body,
        }  # Obviament hem de guardar el contingut d ela funció per futurs accesos
        return func_name

    def visitConstdef(self, ctx):
        const_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.value())
        self.entorn[const_name] = value  # Ídem que Functiondef
        return const_name

    def visitExpression(self, ctx):
        if (
            ctx.IDENTIFIER()
        ):  # Per mirar si ens trobem davant d'una trucada a funció/invocació de constant
            id = ctx.getText()
            if id in self.entorn:
                return self.entorn[id]
        return self.visit(ctx.getChild(0))

    def visitTrucada(self, ctx):
        function_name = ctx.IDENTIFIER().getText()
        # Primer veiem si la funció està definida
        if function_name not in self.entorn:
            raise Exception(f"Funció no definida: {function_name}")
        # Comprobació d'error
        function = self.entorn[function_name]
        if "params" not in function or "body" not in function:
            raise Exception(f"Funció {function_name} no vàlida")

        # Passem paràmetres i contingut de la funció per aplicar-los
        parameters = [self.visit(param) for param in ctx.expression()]
        local_entorn = dict(zip(function["params"], parameters))
        return self.aplica_func(function["body"], local_entorn)

    # En aquesta funció crearem un entorn local per la trucada a la funció el qual després desapareix, seguim l'estructura de pila per fer trucades
    def aplica_func(self, body, local_entorn):
        original_entorn = self.entorn.copy()
        self.entorn.update(local_entorn)
        results = [self.visit(expr) for expr in body]
        self.entorn = original_entorn
        return (
            results[-1] if results else None
        )  # Retornarà el resultat de l'última expressió, si n'hi ha

    def visitValue(self, ctx):
        if ctx.BOOLEAN():
            return True if ctx.BOOLEAN().getText() == "#t" else False
        elif ctx.NUMBER():
            return int(ctx.NUMBER().getText())
        elif ctx.STRING():
            return ctx.STRING().getText().strip('"')
        elif ctx.llista():
            return self.visitLlista(ctx.llista())
        return None

    def visitIofunc(self, ctx):
        funcio = ctx.getChild(1).getText()
        if funcio == "newline":
            print()
            return None
        elif funcio == "read":  # S'han de parsejar els valors d'entrada
            entrada = input().strip()
            if entrada.startswith("'(") and entrada.endswith(")"):
                entrada = entrada[2:-1]
                parsed_list = entrada.split()
                return [self.parseja(x) for x in parsed_list]
            else:
                return self.parseja(entrada)
        else:
            print(self.visit(ctx.expression()))
            return None

    # Auxiliar de parseig simple
    def parseja(self, x):
        if x.isdigit():
            return int(x)
        elif x == "#t":
            return True
        elif x == "#f":
            return False
        else:
            return x

    def visitLlista(self, ctx):
        if len(ctx.value()) == 0:  # Llista buida
            return []
        return [self.visit(value) for value in ctx.value()]

    # Comportament de les funcions de llistes integrades
    def visitListfunc(self, ctx):
        funcio = ctx.listf().getText()
        lista = self.visit(ctx.expression())
        if funcio == "car":
            return lista[0]
        elif funcio == "cdr":
            return lista[1:]
        elif funcio == "null?":
            return len(lista) == 0
        else:
            return [self.visit(ctx.getChild(1))] + lista
        return None

    def visitIfexpr(self, ctx):
        if self.visit(ctx.expression(0)):
            return self.visit(ctx.expression(1))
        else:
            return self.visit(ctx.expression(2))

    def visitCondexpr(self, ctx):
        sz = ctx.getChildCount()
        for cond_clause in range(
            0, sz - 3
        ):  # Mirem totes les possibles clàusules condicionals
            condition = self.visit(ctx.condi(cond_clause))
            if condition is not None:
                return condition
        return None

    def visitCondi(self, ctx):
        condition = self.visit(ctx.expression(0))
        if condition:
            for clau in ctx.expression():
                if clau != ctx.expression(0):
                    self.visit(clau)
            return self.visit(
                ctx.expression(len(ctx.expression()) - 1)
            )  # Retornem últim resultat encara que podem realitzar diverses accions
        return None

    def visitLetexpr(self, ctx):
        original_entorn = self.entorn.copy()  # Utilitzem let per declarar dades locals
        local_entorn = {}

        for var in ctx.letvar():
            name = var.IDENTIFIER().getText()
            value = self.visit(var.expression())
            local_entorn[name] = value

        self.entorn.update(local_entorn)

        for oneex in ctx.expression():
            result = self.visit(oneex)
        self.entorn = original_entorn

        return result

    # Tractament de les funcions aritmètiques predefinides
    def visitAritmexpr(self, ctx):
        operator = ctx.aoperator().getText()
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            return left / right
        elif operator == "mod":
            return left % right

    # Tractament dels operadors lògics integrats
    def visitLogicop(self, ctx):
        operator = ctx.loperator().getText()
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if operator == "<":
            return left < right
        elif operator == ">":
            return left > right
        elif operator == "=":
            return left == right
        elif operator == "<>":
            return left != right
        elif operator == "<=":
            return left <= right
        elif operator == ">=":
            return left >= right

    # Tractament de les portes lògiques integrades
    def visitLogicfunc(self, ctx):
        if len(ctx.expression()) == 2:  # And i or agafen 2 paràmetres, not agafa 1
            operator = ctx.logicdoor().getText()
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))

            if operator == "and":
                return left and right
            elif operator == "or":
                return left or right
        else:
            operator = ctx.getChild(1).getText()
            operand = self.visit(ctx.expression(0))
            if operator == "not":
                return not operand
