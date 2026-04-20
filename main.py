import json
from datetime import datetime


def listar_produtos(self):
    print("\n=== ESTOQUE ===")
    for p in self.produtos.values():
        print(f"{p.nome} | Código: {p.codigo} | Qtde: {p.quantidade} | Validade: {p.validade}")

def verificar_vencimento(self):
    hoje = datetime.now().date()
    print("\n=== VENCIMENTOS ===")

    for p in self.produtos.values():
        validade = datetime.strptime(p.validade, "%Y-%m-%d").date()

        if validade <= hoje:
            print(f"⚠ {p.nome} VENCIDO!")
        elif (validade - hoje).days <= 30:
            print(f"⚠ {p.nome} vence em breve!")


def estoque_baixo(self, limite=5):
    print("\n=== ESTOQUE BAIXO ===")
    for p in self.produtos.values():
        if p.quantidade <= limite:
            print(f"⚠ {p.nome} com {p.quantidade} unidades")

