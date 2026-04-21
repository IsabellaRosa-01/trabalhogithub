"""
Sistema de Farmácia - Controle de estoque e vendas
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict


# -------------------------
# Classe Produto
# -------------------------
@dataclass
class Produto:
    """Representa um produto da farmácia"""

    nome: str
    codigo: str
    quantidade: int
    preco: float
    validade: str

    def to_dict(self):
        """Converte o produto para dicionário"""
        return asdict(self)


# -------------------------
# Sistema
# -------------------------
class SistemaFarmacia:
    """Sistema principal de controle da farmácia"""

    def __init__(self):
        self.produtos = {}
        self.vendas = []
        self.usuarios = {"admin": "123"}
        self.carregar()

    # -------------------------
    # Persistência
    # -------------------------
    def salvar(self):
        """Salva dados em arquivos JSON"""
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
        """Carrega dados dos arquivos JSON"""
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
    # Login
    # -------------------------
    def login(self):
        """Realiza autenticação do usuário"""
        print("\n=== LOGIN ===")
        user = input("Usuário: ")
        senha = input("Senha: ")

        if user in self.usuarios and self.usuarios[user] == senha:
            print("✔ Login realizado com sucesso!")
            return True

        print("❌ Usuário ou senha inválidos!")
        return False

    # -------------------------
    # Cadastro
    # -------------------------
    def cadastrar_produto(self):
        """Cadastra um novo produto"""
        nome = input("Nome: ")
        codigo = input("Código: ")

        if codigo in self.produtos:
            print("⚠ Produto já existe!")
            return

        try:
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
        except ValueError:
            print("⚠ Valores inválidos!")
            return

        validade = input("Validade (YYYY-MM-DD): ")

        try:
            datetime.strptime(validade, "%Y-%m-%d")
        except ValueError:
            print("⚠ Data inválida!")
            return

        self.produtos[codigo] = Produto(
            nome=nome,
            codigo=codigo,
            quantidade=quantidade,
            preco=preco,
            validade=validade,
        )

        self.salvar()
        print("✔ Produto cadastrado!")

    # -------------------------
    # Entrada
    # -------------------------
    def entrada(self):
        """Registra entrada de estoque"""
        codigo = input("Código: ")

        if codigo not in self.produtos:
            print("⚠ Produto não encontrado!")
            return

        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("⚠ Valor inválido!")
            return

        self.produtos[codigo].quantidade += quantidade
        self.salvar()
        print("✔ Entrada registrada!")

    # -------------------------
    # Venda
    # -------------------------
    def vender(self):
        """Realiza venda de produto"""
        codigo = input("Código: ")

        if codigo not in self.produtos:
            print("⚠ Produto não encontrado!")
            return

        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("⚠ Valor inválido!")
            return

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
            "data": datetime.now().strftime("%Y-%m-%d"),
        }

        self.vendas.append(venda)
        self.salvar()
        print("✔ Venda realizada!")

    # -------------------------
    # Listar
    # -------------------------
    def listar_produtos(self):
        """Lista produtos em estoque"""
        print("\n=== ESTOQUE ===")
        for p in self.produtos.values():
            print(
                f"{p.nome} | Código: {p.codigo} | "
                f"Qtde: {p.quantidade} | Validade: {p.validade}"
            )

    # -------------------------
    # Alertas
    # -------------------------
    def verificar_vencimento(self):
        """Verifica produtos vencidos ou próximos do vencimento"""
        hoje = datetime.now().date()
        print("\n=== VENCIMENTOS ===")

        for p in self.produtos.values():
            validade = datetime.strptime(p.validade, "%Y-%m-%d").date()

            if validade <= hoje:
                print(f"⚠ {p.nome} VENCIDO!")
            elif (validade - hoje).days <= 30:
                print(f"⚠ {p.nome} vence em breve!")

    def estoque_baixo(self, limite=5):
        """Lista produtos com estoque baixo"""
        print("\n=== ESTOQUE BAIXO ===")
        for p in self.produtos.values():
            if p.quantidade <= limite:
                print(f"⚠ {p.nome} com {p.quantidade} unidades")

    # -------------------------
    # Relatório
    # -------------------------
    def relatorio_vendas(self):
        """Gera relatório de vendas por período"""
        print("\n=== RELATÓRIO DE VENDAS ===")

        data_inicio = input("Data início (YYYY-MM-DD): ")
        data_fim = input("Data fim (YYYY-MM-DD): ")

        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            fim = datetime.strptime(data_fim, "%Y-%m-%d")
        except ValueError:
            print("⚠ Data inválida!")
            return

        total = 0

        for v in self.vendas:
            data = datetime.strptime(v["data"], "%Y-%m-%d")

            if inicio <= data <= fim:
                print(
                    f"{v['data']} | {v['nome']} | "
                    f"Qtde: {v['quantidade']} | R$ {v['total']}"
                )
                total += v["total"]

        print(f"\n💰 Total: R$ {total:.2f}")

# -------------------------
# Menu
# -------------------------
def menu():
    """Menu principal do sistema"""
    sistema = SistemaFarmacia()

    if not sistema.login():
        return

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar produto")
        print("2 - Entrada de estoque")
        print("3 - Vender produto")
        print("4 - Listar produtos")
        print("5 - Verificar vencimentos")
        print("6 - Estoque baixo")
        print("7 - Relatório de vendas")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            sistema.cadastrar_produto()
        elif op == "2":
            sistema.entrada()
        elif op == "3":
            sistema.vender()
        elif op == "4":
            sistema.listar_produtos()
        elif op == "5":
            sistema.verificar_vencimento()
        elif op == "6":
            sistema.estoque_baixo()
        elif op == "7":
            sistema.relatorio_vendas()
        elif op == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()
