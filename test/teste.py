from src.main import SistemaFarmacia, Produto
import unittest
from unittest.mock import patch
import os


class TestSistemaFarmacia(unittest.TestCase):

    def setUp(self):
        # Evita interferência de arquivos reais
        self.sistema = SistemaFarmacia()
        self.sistema.produtos = {}
        self.sistema.vendas = []

    # -------------------------
    # Teste Produto
    # -------------------------
    def test_produto_to_dict(self):
        produto = Produto("Dipirona", "001", 10, 5.0, "2025-12-31")
        dicionario = produto.to_dict()

        self.assertEqual(dicionario["nome"], "Dipirona")
        self.assertEqual(dicionario["codigo"], "001")

    # -------------------------
    # Teste Login
    # -------------------------
    @patch("builtins.input", side_effect=["admin", "123"])
    def test_login_sucesso(self, mock_input):
        self.assertTrue(self.sistema.login())

    @patch("builtins.input", side_effect=["admin", "errado"])
    def test_login_falha(self, mock_input):
        self.assertFalse(self.sistema.login())

    # -------------------------
    # Teste Cadastro Produto
    # -------------------------
    @patch("builtins.input", side_effect=["Paracetamol", "123", "10", "5.5", "2025-12-31"])
    def test_cadastrar_produto(self, mock_input):
        self.sistema.cadastrar_produto()
        self.assertIn("123", self.sistema.produtos)

    # -------------------------
    # Teste Entrada
    # -------------------------
    @patch("builtins.input", side_effect=["123", "5"])
    def test_entrada_estoque(self, mock_input):
        self.sistema.produtos["123"] = Produto("Teste", "123", 10, 5.0, "2025-12-31")
        self.sistema.entrada()
        self.assertEqual(self.sistema.produtos["123"].quantidade, 15)

    # -------------------------
    # Teste Venda
    # -------------------------
    @patch("builtins.input", side_effect=["123", "5"])
    def test_vender_produto(self, mock_input):
        self.sistema.produtos["123"] = Produto("Teste", "123", 10, 5.0, "2025-12-31")
        self.sistema.vender()

        self.assertEqual(self.sistema.produtos["123"].quantidade, 5)
        self.assertEqual(len(self.sistema.vendas), 1)

    # -------------------------
    # Teste Venda com estoque insuficiente
    # -------------------------
    @patch("builtins.input", side_effect=["123", "20"])
    def test_venda_estoque_insuficiente(self, mock_input):
        self.sistema.produtos["123"] = Produto("Teste", "123", 10, 5.0, "2025-12-31")
        self.sistema.vender()

        self.assertEqual(self.sistema.produtos["123"].quantidade, 10)
        self.assertEqual(len(self.sistema.vendas), 0)

    # -------------------------
    # Teste Relatório
    # -------------------------
    @patch("builtins.input", side_effect=["2020-01-01", "2030-01-01"])
    def test_relatorio_vendas(self, mock_input):
        self.sistema.vendas.append({
            "codigo": "123",
            "nome": "Teste",
            "quantidade": 2,
            "total": 10.0,
            "data": "2025-01-01"
        })

        # Só verifica se roda sem erro
        self.sistema.relatorio_vendas()


if __name__ == "__main__":
    unittest.main()