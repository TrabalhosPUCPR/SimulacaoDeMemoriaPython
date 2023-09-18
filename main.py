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

from cache_lines import CacheLines
from cache import Cache
from cpu import CPU
from in_out import IO
from memoria import EnderecoInvalido
from ram import RAM


def main():
    try:
        io = IO()
        ram = RAM(22)  # 4M de RAM (2**22)
        cache = CacheLines(4 * 2 ** 10, 64, ram)  # total cache = 4K, cacheline = 64
        cpu = CPU(cache, io)

        inicio = 0

        print("Programa 1")
        ram.write(inicio, 118)
        ram.write(inicio + 1, 130)
        cpu.run(inicio)

        print("\nPrograma 2")
        cache.write(inicio, 4155)
        cache.write(inicio + 1, 4165)
        cpu.run(inicio)
    except EnderecoInvalido as e:
        print("Endereco inválido:", e.ender, file=sys.stderr)


if __name__ == '__main__':
    main()
