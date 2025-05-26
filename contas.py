import json
import os

class GerenciadorContas:
    def __init__(self):
        self.arquivo_contas = "contas_salvas.json"
        self.contas = self.carregar_contas()

    def carregar_contas(self):
        if os.path.exists(self.arquivo_contas):
            try:
                with open(self.arquivo_contas, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def salvar_conta(self, nome, dados):
        self.contas[nome] = dados
        with open(self.arquivo_contas, 'w') as f:
            json.dump(self.contas, f, indent=4)

    def remover_conta(self, nome):
        if nome in self.contas:
            del self.contas[nome]
            with open(self.arquivo_contas, 'w') as f:
                json.dump(self.contas, f, indent=4)

    def obter_contas(self):
        return list(self.contas.keys())

    def obter_dados_conta(self, nome):
        return self.contas.get(nome, None)