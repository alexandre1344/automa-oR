import requests
import os
import sys
from version import VERSION
import tempfile
import zipfile
import shutil

class Updater:
    def __init__(self):
        self.current_version = VERSION
        self.github_repo = "seu_usuario/seu_repositorio"  # Substitua pelo seu repositório
        self.update_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        
    def check_for_updates(self):
        try:
            response = requests.get(self.update_url)
            latest_version = response.json()["tag_name"]
            
            if self._compare_versions(latest_version, self.current_version):
                return True, latest_version
            return False, None
        except Exception as e:
            print(f"Erro ao verificar atualizações: {e}")
            return False, None
    
    def download_update(self, version):
        try:
            # URL do arquivo zip da nova versão
            download_url = f"https://github.com/{self.github_repo}/releases/download/{version}/AutomacaoRAS.zip"
            
            # Download do arquivo
            response = requests.get(download_url, stream=True)
            
            # Criar pasta temporária
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")
            
            # Salvar arquivo
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            # Extrair arquivo
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            # Copiar arquivos novos
            self._update_files(temp_dir)
            
            # Limpar arquivos temporários
            shutil.rmtree(temp_dir)
            
            return True
        except Exception as e:
            print(f"Erro ao baixar atualização: {e}")
            return False
    
    def _compare_versions(self, v1, v2):
        # Compara versões (retorna True se v1 > v2)
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        return v1_parts > v2_parts
    
    def _update_files(self, temp_dir):
        # Copia os arquivos novos para a pasta do programa
        current_dir = os.path.dirname(sys.executable)
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file != "update.zip":
                    src = os.path.join(root, file)
                    dst = os.path.join(current_dir, file)
                    shutil.copy2(src, dst)