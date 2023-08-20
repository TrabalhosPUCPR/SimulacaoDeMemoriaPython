from memoria import Memoria, EnderecoInvalido


class Cache(Memoria):
    def __init__(self, tamanho, ram):
        super().__init__(tamanho)
        self.memoria = [0] * tamanho
        self.ram = ram
        self.modificado = False
        self.ram_addr = 0

    def read(self, ender):
        try:
            self.verifica_endereco(ender)
            print("CACHE READ HIT: ", ender)
            return self.memoria[ender - self.ram_addr]
        except EnderecoInvalido:
            self.ram.verifica_endereco(ender)
            print("CACHE READ MISS: ", ender)
            if self.modificado:
                self.move_to_ram()
                self.modificado = False
            self.copy_from_ram(ender)
            return self.memoria[ender - self.ram_addr]

    def verifica_endereco(self, ender):
        if (ender < self.ram_addr) or (ender >= self.ram_addr + self.tamanho()):
            raise EnderecoInvalido(ender)

    def write(self, ender, val):
        try:
            self.verifica_endereco(ender)
            print("CACHE WRITE HIT: ", ender)
            self.memoria[ender - self.ram_addr] = val
        except EnderecoInvalido:
            self.ram.verifica_endereco(ender)
            print("CACHE WRITE MISS: ", ender)
            if self.modificado:
                self.move_to_ram()
            self.copy_from_ram(ender)
            self.memoria[ender - self.ram_addr] = val
        self.modificado = True

    def move_to_ram(self):
        c = 0
        while c < self.tamanho():
            self.ram.write(self.ram_addr + c, self.memoria[c])
            self.memoria[c] = 0
            c += 1

    def copy_from_ram(self, pos):
        self.ram_addr = pos
        c = 0
        try:
            self.ram.verifica_endereco(self.ram_addr + self.tamanho() - 1)
        except EnderecoInvalido:
            self.ram_addr = self.ram.tamanho() - self.tamanho()
        while c < self.tamanho():
            val = self.ram.read(self.ram_addr + c)
            self.memoria[c] = val
            c += 1
