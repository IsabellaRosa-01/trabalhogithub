import json
from datetime import datetime
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