from src.main import *
import unittest

class TestSistemaFarmacia(unittest.TestCase):

    def setUp(self):
        self.sistema = SistemaFarmacia()
        self.sistema.produtos = {}
        self.sistema.vendas = []

    def test_login(self):
        self.assertTrue(self.sistema.login("admin", "123"))
        self.assertFalse(self.sistema.login("admin", "errado"))

    def test_cadastrar_produto(self):
        result = self.sistema.cadastrar_produto(
            "Dipirona", "001", 10, 5.0, "2025-12-31"
        )
        self.assertTrue(result)
        self.assertIn("001", self.sistema.produtos)

    def test_produto_duplicado(self):
        self.sistema.cadastrar_produto("A", "001", 10, 5.0, "2025-12-31")
        result = self.sistema.cadastrar_produto("B", "001", 10, 5.0, "2025-12-31")
        self.assertFalse(result)

    def test_entrada(self):
        self.sistema.cadastrar_produto("A", "001", 10, 5.0, "2025-12-31")
        self.sistema.entrada("001", 5)
        self.assertEqual(self.sistema.produtos["001"].quantidade, 15)

    def test_venda(self):
        self.sistema.cadastrar_produto("A", "001", 10, 5.0, "2025-12-31")
        result = self.sistema.vender("001", 5)

        self.assertTrue(result)
        self.assertEqual(self.sistema.produtos["001"].quantidade, 5)
        self.assertEqual(len(self.sistema.vendas), 1)

    def test_venda_erro(self):
        self.sistema.cadastrar_produto("A", "001", 10, 5.0, "2025-12-31")
        result = self.sistema.vender("001", 20)

        self.assertFalse(result)
        self.assertEqual(len(self.sistema.vendas), 0)

    def test_estoque_baixo(self):
        self.sistema.cadastrar_produto("A", "001", 3, 5.0, "2025-12-31")
        baixos = self.sistema.estoque_baixo()
        self.assertEqual(len(baixos), 1)

    def test_relatorio(self):
        self.sistema.cadastrar_produto("A", "001", 10, 5.0, "2025-12-31")
        self.sistema.vender("001", 2)

        rel, total = self.sistema.relatorio_vendas("2020-01-01", "2030-01-01")

        self.assertEqual(len(rel), 1)
        self.assertEqual(total, 10.0)


if __name__ == "__main__":
    unittest.main()
    