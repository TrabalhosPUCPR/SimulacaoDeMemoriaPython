#!/usr/bin/env python3

#
# von Neumann - Arquitetura Básica
# Todos as classes em um mesmo arquivo
# PSCF - Prof. Luiz Lima Jr.
#
# Arquitetura formada de 3 componentes básicos:
#
# 1. Memória => RAM
# 2. CPU
# 3. Entrada e Saída (IO)
#

import sys

from CacheLines import CacheLines
from cache import Cache
from cpu import CPU
from in_out import IO
from memoria import EnderecoInvalido
from ram import RAM


def main():
    try:
        io = IO(sys.stdin, sys.stdout)
        ram = RAM(7)
        cache = CacheLines(4 * 2**10, 64, ram)
        cpu = CPU(cache, io)

        inicio = 10
        cache.write(inicio, 118)
        ram.write(inicio + 1, 130)
        cpu.run(inicio)
    except EnderecoInvalido as e:
        print("Endereço inválido:", e.ender, file=sys.stderr)


if __name__ == '__main__':
    main()
