import json
from datetime import datetime


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

