import json
from datetime import datetime
# -------------------------
# Classe Produto
# -------------------------
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

    # -------------------------
    # Login
    # -------------------------
    def login(self):
        print("\n=== LOGIN ===")
        user = input("Usuário: ")
        senha = input("Senha: ")

        if user in self.usuarios and self.usuarios[user] == senha:
            print("✔ Login realizado com sucesso!")
            return True
        else:
            print("❌ Usuário ou senha inválidos!")
            return False

    # -------------------------
    # Cadastro
    # -------------------------
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

    # -------------------------
    # Entrada
    # -------------------------
    def entrada(self):
        codigo = input("Código: ")
        if codigo not in self.produtos:
            print("⚠ Produto não encontrado!")
            return

        quantidade = int(input("Quantidade: "))
        self.produtos[codigo].quantidade += quantidade
        self.salvar()
        print("✔ Entrada registrada!")

    # -------------------------
    # Venda (Saída)
    # -------------------------
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

    # -------------------------
    # Listar
    # -------------------------
    def listar_produtos(self):
        print("\n=== ESTOQUE ===")
        for p in self.produtos.values():
            print(f"{p.nome} | Código: {p.codigo} | Qtde: {p.quantidade} | Validade: {p.validade}")

    # -------------------------
    # Alertas
    # -------------------------
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

    # -------------------------
    # Relatório
    # -------------------------
    def relatorio_vendas(self):
        print("\n=== RELATÓRIO DE VENDAS ===")

        data_inicio = input("Data início (YYYY-MM-DD): ")
        data_fim = input("Data fim (YYYY-MM-DD): ")

        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            fim = datetime.strptime(data_fim, "%Y-%m-%d")
        except:
            print("⚠ Data inválida!")
            return

        total = 0

        for v in self.vendas:
            data = datetime.strptime(v["data"], "%Y-%m-%d")

            if inicio <= data <= fim:
                print(f"{v['data']} | {v['nome']} | Qtde: {v['quantidade']} | R$ {v['total']}")
                total += v["total"]

        print(f"\n💰 Total: R$ {total:.2f}")


# -------------------------
# Menu
# -------------------------
def menu():
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
    