from memoria import Memoria
import numpy as np


class CacheLines(Memoria):
    class Line:
        def __init__(self, t, w):
            self.t = t
            self.w = w

    def read(self, ender):
        print(self.extract_w_r_t(ender))
        pass

    def write(self, ender, val):
        print(self.extract_w_r_t(ender))
        pass

    def __init__(self, size, lines, ram):
        super().__init__(size)
        self.lines = [None] * lines
        self.ram = ram
        self.size = np.log2(ram.tamanho())
        self.word_size = int(np.log2(lines))
        self.row_size = int(np.log2(size))
        self.tag_size = int((self.word_size + self.row_size) - np.log2(ram.tamanho()))

    def extract_w_r_t(self, ender: int):
        a = int("1" * self.word_size)
        w = bin(ender & a)
        ender = ender << self.word_size
        r = ender & int("1" * self.row_size)
        ender = ender << self.row_size
        t = ender & int("1" * self.tag_size)
        return w, r, t
