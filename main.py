import json
from datetime import datetime
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
