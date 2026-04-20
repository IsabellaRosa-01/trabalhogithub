import json
from datetime import datetime
class Produto:
    def __init__(self, nome, codigo, quantidade, preco, validade):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.preco = preco
        self.validade = validade

    def to_dict(self):
        return self.__dict__


# -------------------------
# Sistema
# -------------------------
class SistemaFarmacia:
    def __init__(self):
        self.produtos = {}
        self.vendas = []
        self.usuarios = {"admin": "123"}
        self.carregar()

    # -------------------------
    # Persistência
    # -------------------------
    def salvar(self):
        with open("estoque.json", "w") as f:
            json.dump({k: v.to_dict() for k, v in self.produtos.items()}, f, indent=4)

        with open("vendas.json", "w") as f:
            json.dump(self.vendas, f, indent=4)

    def carregar(self):
        try:
            with open("estoque.json", "r") as f:
                dados = json.load(f)
                for k, v in dados.items():
                    self.produtos[k] = Produto(**v)
        except:
            pass

        try:
            with open("vendas.json", "r") as f:
                self.vendas = json.load(f)
        except:
            pass
