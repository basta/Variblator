from lark import Lark, Transformer, v_args

GRAMMAR = """
?start: sum
      | NAME "=" sum    -> assign_var

?sum: product
    | sum "+" product   -> add
    | sum "-" product   -> sub

?product: atom
    | product "*" atom  -> mul
    | product "/" atom  -> div
    | product "%" atom  -> mod
    | product "^" atom  -> pow

?atom: NUMBER           -> number
     | "-" atom         -> neg
     | NAME             -> var
     | "(" sum ")"

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE

%ignore WS_INLINE
"""


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg, pow, mod

    number = float

    def __init__(self):
        super(CalculateTree, self).__init__()
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception(f"Variable not found: {name}")


calc_parser = Lark(GRAMMAR, parser="lalr", transformer=CalculateTree())
calc = calc_parser.parse


def parse_text(lines: list[str]) -> list[str]:

    ret = []
    for line in lines:
        if isinstance(line, float):
            ret.append(str(f"{line:0.4}"))
        try:
            ret.append(str(calc(line)))
        except:
            ret.append("")
    return ret
