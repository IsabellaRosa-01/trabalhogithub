import json
from datetime import datetime


def entrada(self):
    codigo = input("Código: ")
    if codigo not in self.produtos:
        print("⚠ Produto não encontrado!")
        return

    quantidade = int(input("Quantidade: "))
    self.produtos[codigo].quantidade += quantidade
    self.salvar()
    print("✔ Entrada registrada!")

def vender(self):
    codigo = input("Código: ")

    if codigo not in self.produtos:
        print("⚠ Produto não encontrado!")
        return

    quantidade = int(input("Quantidade: "))
    produto = self.produtos[codigo]

    if produto.quantidade < quantidade:
        print("⚠ Estoque insuficiente!")
        return

    produto.quantidade -= quantidade

    venda = {
        "codigo": codigo,
        "nome": produto.nome,
        "quantidade": quantidade,
        "total": quantidade * produto.preco,
        "data": datetime.now().strftime("%Y-%m-%d")
    }

    self.vendas.append(venda)
    self.salvar()
    print("✔ Venda realizada!")
