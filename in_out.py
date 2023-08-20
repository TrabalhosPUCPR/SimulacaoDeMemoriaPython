import sys


class IO:
    def __init__(self, entrada=sys.stdin, saida=sys.stdout):
        # saída-padrão = tela (stdout)
        self.entrada = entrada
        self.saida = saida

    def output(self, s):
        print(s, end='', file=self.saida)
