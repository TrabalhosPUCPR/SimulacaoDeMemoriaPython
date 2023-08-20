# Exceção (erro)
from abc import abstractmethod


class EnderecoInvalido(Exception):
    def __init__(self, ender):
        self.ender = ender

    def __repr__(self):
        return self.ender


class Memoria:
    def __init__(self, capacidade):
        self._capacidade = capacidade

    def verifica_endereco(self, ender):
        if (ender < 0) or (ender >= self._capacidade):
            raise EnderecoInvalido(ender)

    def tamanho(self):
        return self._capacidade

    # métodos abstratos devem ser sobrescritos pelas subclasses

    @abstractmethod
    def read(self, ender): pass

    @abstractmethod
    def write(self, ender, val): pass
