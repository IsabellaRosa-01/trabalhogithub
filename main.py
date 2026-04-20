import json
from datetime import datetime

def cadastrar_produto(self):
    nome = input("Nome: ")
    codigo = input("Código: ")

    if codigo in self.produtos:
        print("⚠ Produto já existe!")
        return

    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))
    validade = input("Validade (YYYY-MM-DD): ")

    try:
        datetime.strptime(validade, "%Y-%m-%d")
    except:
        print("⚠ Data inválida!")
        return

    self.produtos[codigo] = Produto(nome, codigo, quantidade, preco, validade)
    self.salvar()
    print("✔ Produto cadastrado!")