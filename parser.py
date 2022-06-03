from lark import Lark, Transformer, v_args


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg

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


calc_parser = Lark(
    open("grammar.lark").read(), parser="lalr", transformer=CalculateTree()
)
calc = calc_parser.parse


def parse_text(lines: list[str]) -> list[str]:
    ret = []
    for line in lines:
        try:
            ret.append(str(calc(line)))
        except:
            ret.append("ERR")
    return ret
