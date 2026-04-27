"""
Sistema de Farmácia - Controle de estoque e vendas
"""
import json
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Produto:
    """Representa um produto da farmácia"""
    nome: str
    codigo: str
    quantidade: int
    preco: float
    validade: str

    def to_dict(self):
        return asdict(self)


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
        with open("estoque.json", "w", encoding="utf-8") as f:
            json.dump(
                {k: v.to_dict() for k, v in self.produtos.items()},
                f,
                indent=4,
                ensure_ascii=False,
            )

        with open("vendas.json", "w", encoding="utf-8") as f:
            json.dump(self.vendas, f, indent=4, ensure_ascii=False)

    def carregar(self):
        try:
            with open("estoque.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                for k, v in dados.items():
                    self.produtos[k] = Produto(**v)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        try:
            with open("vendas.json", "r", encoding="utf-8") as f:
                self.vendas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    # -------------------------
    # Lógica (TESTÁVEL)
    # -------------------------
    def login(self, user, senha):
        return user in self.usuarios and self.usuarios[user] == senha

    def cadastrar_produto(self, nome, codigo, quantidade, preco, validade):
        """Cadastra um novo produto no sistema"""
        if codigo in self.produtos:
            return False

        try:
            datetime.strptime(validade, "%Y-%m-%d")
        except ValueError:
            return False

        self.produtos[codigo] = Produto(nome, codigo, quantidade, preco, validade)
        return True

    def entrada(self, codigo, quantidade):
        if codigo not in self.produtos:
            return False

        self.produtos[codigo].quantidade += quantidade
        return True

    def vender(self, codigo, quantidade):
        if codigo not in self.produtos:
            return False

        produto = self.produtos[codigo]

        if produto.quantidade < quantidade:
            return False

        produto.quantidade -= quantidade

        venda = {
            "codigo": codigo,
            "nome": produto.nome,
            "quantidade": quantidade,
            "total": quantidade * produto.preco,
            "data": datetime.now().strftime("%Y-%m-%d"),
        }

        self.vendas.append(venda)
        return True

    def listar_produtos(self):
        return list(self.produtos.values())

    def verificar_vencimento(self):
        hoje = datetime.now().date()
        resultado = []

        for p in self.produtos.values():
            validade = datetime.strptime(p.validade, "%Y-%m-%d").date()

            if validade <= hoje:
                resultado.append((p.nome, "vencido"))
            elif (validade - hoje).days <= 30:
                resultado.append((p.nome, "proximo"))

        return resultado

    def estoque_baixo(self, limite=5):
        return [p for p in self.produtos.values() if p.quantidade <= limite]

    def relatorio_vendas(self, data_inicio, data_fim):
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            fim = datetime.strptime(data_fim, "%Y-%m-%d")
        except ValueError:
            return None

        resultado = []
        total = 0

        for v in self.vendas:
            data = datetime.strptime(v["data"], "%Y-%m-%d")

            if inicio <= data <= fim:
                resultado.append(v)
                total += v["total"]

        return resultado, total


# -------------------------
# Interface (CLI)
# -------------------------
def menu():
    sistema = SistemaFarmacia()

    user = input("Usuário: ")
    senha = input("Senha: ")

    if not sistema.login(user, senha):
        print("Login inválido")
        return

    while True:
        print("\n1 - Cadastrar produto")
        print("2 - Entrada")
        print("3 - Venda")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            nome = input("Nome: ")
            codigo = input("Código: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            validade = input("Validade: ")

            if sistema.cadastrar_produto(nome, codigo, quantidade, preco, validade):
                sistema.salvar()
                print("OK")
            else:
                print("Erro")

        elif op == "2":
            codigo = input("Código: ")
            quantidade = int(input("Quantidade: "))

            if sistema.entrada(codigo, quantidade):
                sistema.salvar()
                print("OK")
            else:
                print("Erro")

        elif op == "3":
            codigo = input("Código: ")
            quantidade = int(input("Quantidade: "))

            if sistema.vender(codigo, quantidade):
                sistema.salvar()
                print("OK")
            else:
                print("Erro")

        elif op == "0":
            break


if __name__ == "__main__":
    menu()
