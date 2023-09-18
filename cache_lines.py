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
        # eu nao vou escrever tudo de novo aqui, os comentario disso ta no write()
        # a unica diferenca é que ao inves de setar o valor passado como parametro, a gente retorna o valor encontrado
        # (por isso que é read (⊙ˍ⊙))
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
            self.lines[r] = self.copy_block_from_ram(self.lines[r], ender, t)
            return self.lines[r].words[w]

    def copy_block_to_ram(self, block, s):

        # seta o bloco como nao modificado
        block.modif = 0
        for i in block.words:
            self.ram.write(s, i)
            s += 1

    def copy_block_from_ram(self, line, ram_address, t):
        # copia o bloco no endereco da ram passado como parametro e o insere na linha
        # pega o valor maximo da quantidade de bits de uma linha, e itera sobre ela
        for i in range(2 ** self.word_size):
            # da read do valor no endereco da memoria ram e passa para o bloco
            line.words[i] = self.ram.read(ram_address)

            # incrementa 1 no endereco, para pegar a proxima posicao
            ram_address += 1

        # seta a nova tag para o bloco
        line.t = t
        return line

    def write(self, ender, val):
        # extrai os valores do endereco da ram passado como parametro
        w, r, t, s = self.extract_w_r_t_s(ender)
        try:
            # verifica se o endereco r esta dentro da cache
            self.verifica_endereco(r)

            # passa a linha para uma variavel para facilitar nossa vida
            row = self.lines[r]

            # compara a tag da linha encontrada, com a tag extraida do endereco
            # caso for falso, o endereco nao esta dentro do bloco
            # caso for verdadeiro, o endereco esta dentro do bloco
            if row.t != t:
                raise EnderecoInvalido(ender)
            print(f"WRITE CACHE HIT: {self._get_line_info(ender, r)}")

            # escreve o valor passado como parametro para o endereco encontrado dentro da linha
            self.lines[r].words[w] = val

            # marca a linha como modificado
            self.lines[r].modif = 1
        except EnderecoInvalido:
            print(f"WRITE CACHE MISS: {self._get_line_info(ender, r)}")

            # verifica se a linha foi modificada, caso for, move a linha para sua respectiva posicao dentro da ram e
            # seta ela como nao modificado
            if self.lines[r].modif:
                self.copy_block_to_ram(self.lines[r], s)
                self.lines[r].modif = False

            # pega o bloco que comeca no endereco e coloca ela para dentro da cache
            self.lines[r] = self.copy_block_from_ram(self.lines[r], ender, t)

            # escreve o valor passado como paramentro para sua posicao correta
            self.lines[r].words[w] = val

    def _get_line_info(self, addr, row):
        # funcao helper apenas para printar dados de uma linha
        words = row * 2 ** self.word_size
        return f"{addr} L{row} block: [{words}...{words + len(self.lines) - 1}]"

    # K
    def __init__(self, size, k, ram):
        super().__init__(size)
        self.ram = ram

        # BLOCO == LINHA

        # bit_size: quantidade de bits para representar um endereco da memoria principal
        self.bit_size = np.log2(ram.tamanho())

        # word_size: quantidade de bits para representar o endereco de um valor dentro do bloco da cache
        self.word_size = int(np.log2(k))

        # lines: array das linhas da cache
        self.lines = []

        # inicializando as linhas, O TAMANHO DO ARRAY NAO É IGUAL AO size !!!
        # como vai ter k valores dentro de cada linha, a gente faz size / k
        # k e a quantidade de palavras de cada linha
        for i in range((int(size / k))):
            # a gente passa a classe Line pra facilita um pouco a nossa vida
            # pra cria a linha a gente so passa o tamanho que ela vai ter (k) e adiciona dentro do array da cache
            self.lines.append(CacheLines.Line(k))

        # row_size: quantidade de bits para representar o endereco de um bloco da cache
        self.row_size = int(np.log2(len(self.lines)))

        # tag_size: quantidade de bits para representar a informacao adicional de um bloco para verificar
        # se um endereco esta dentro do bloco
        self.tag_size = int(self.bit_size - (self.word_size + self.row_size))

    def extract_w_r_t_s(self, ender: int):
        # W - word: endereco do valor dentro do bloco
        # R - row: endereco do bloco dentro da cache
        # T - tag: informacao do bloco para verificar se o endereco esta dentro dele
        # S - sam?: endereco do bloco dentro da memoria principal
        w = ender & (2 ** self.word_size) - 1
        r = (ender >> self.word_size) & (2 ** self.row_size) - 1
        t = (ender >> (self.row_size + self.word_size)) & (2 ** self.tag_size) - 1
        s = (ender >> self.word_size) << self.word_size
        return w, r, t, s
