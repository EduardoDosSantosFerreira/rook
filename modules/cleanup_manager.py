# modules/cleanup_manager.py
import os
import shutil
import tempfile
from pathlib import Path

class CleanupManager:
    """Gerencia limpeza de arquivos temporários"""
    
    def clean_temp_files(self):
        """Limpa arquivos temporários do sistema"""
        try:
            # Limpar temp do usuário
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    self._clean_directory(temp_dir)
            
            # Limpar arquivos .tmp em locais comuns
            self._clean_tmp_files()
            
            return True
        except Exception as e:
            print(f"Erro na limpeza: {e}")
            return False
            
    def _clean_directory(self, directory):
        """Limpa um diretório específico"""
        try:
            for item in Path(directory).glob('*'):
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                except:
                    continue
        except:
            pass
            
    def _clean_tmp_files(self):
        """Limpa arquivos .tmp em locais comuns"""
        drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
                 if os.path.exists(f"{d}:\\")]
        
        for drive in drives:
            try:
                for root, dirs, files in os.walk(drive):
                    for file in files:
                        if file.lower().endswith('.tmp'):
                            try:
                                os.remove(os.path.join(root, file))
                            except:
                                continue
            except:
                continue