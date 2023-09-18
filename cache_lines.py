from memoria import Memoria, EnderecoInvalido
import numpy as np


class CacheLines(Memoria):
    class Line:
        def __init__(self, size, t="", words=None):
            if words is None:
                words = [0] * size
            self.t = t
            self.modif = 0
            self.words = words

    def read(self, ender):
        w, r, t, s = self.extract_w_r_t_s(ender)
        try:
            self.verifica_endereco(r)
            row = self.lines[r]
            if row.t != t:
                raise EnderecoInvalido(ender)
            print(f"READ CACHE HIT: {self._get_line_info(ender, r)}")
            return row.words[w]
        except EnderecoInvalido:
            print(f"READ CACHE MISS: {self._get_line_info(ender, r)}")
            if self.lines[r].modif:
                self.copy_block_to_ram(self.lines[r], s)
            self.lines[r] = self.copy_block_from_ram(self.lines[r], s, t)
            return self.lines[r].words[w]

    def copy_block_to_ram(self, block, s):
        block.modif = 0
        for i in block.words:
            self.ram.write(s, i)
            s += 1

    def copy_block_from_ram(self, line, s, t):
        for i in range(2 ** self.word_size):
            line.words[i] = self.ram.read(s)
            s += 1
        line.t = t
        return line

    def write(self, ender, val):
        w, r, t, s = self.extract_w_r_t_s(ender)
        try:
            self.verifica_endereco(r)
            row = self.lines[r]
            if row.t != t:
                raise EnderecoInvalido(ender)
            print(f"WRITE CACHE HIT: {self._get_line_info(ender, r)}")
            self.lines[r].words[w] = val
            self.lines[r].modif = 1
        except EnderecoInvalido:
            print(f"WRITE CACHE MISS: {self._get_line_info(ender, r)}")
            if self.lines[r].modif:
                self.copy_block_to_ram(self.lines[r], s)
            self.lines[r] = self.copy_block_from_ram(self.lines[r], s, t)
            self.lines[r].words[w] = val

    def _get_line_info(self, addr, row):
        words = row*2**self.word_size
        return f"{addr} L{row} block: [{words}...{words + len(self.lines)}]"

    # K
    def __init__(self, size, k, ram):
        super().__init__(size)
        self.ram = ram
        self.bit_size = np.log2(ram.tamanho())
        self.word_size = int(np.log2(k))
        self.lines = []
        for i in range((int(size / k))):
            self.lines.append(CacheLines.Line(k))
        self.row_size = int(np.log2(len(self.lines)))
        self.tag_size = int(self.bit_size - (self.word_size + self.row_size))

    def extract_w_r_t_s(self, ender: int):
        w = ender & (2 ** self.word_size) - 1
        r = (ender >> self.word_size) & (2 ** self.row_size) - 1
        t = (ender >> (self.row_size + self.word_size)) & (2 ** self.tag_size) - 1
        s = (ender >> self.word_size) << self.word_size
        return w, r, t, s
