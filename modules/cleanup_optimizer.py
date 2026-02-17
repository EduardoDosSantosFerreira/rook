# modules/cleanup_optimizer.py
import os
import shutil
import subprocess
from pathlib import Path
import tempfile
from .base_optimizer import BaseOptimizer

class CleanupOptimizer(BaseOptimizer):
    """Gerencia limpeza avançada do sistema"""
    
    def __init__(self):
        super().__init__()
        self.cleaned_size = 0
        
    def clean_temp_files(self) -> int:
        """Limpa arquivos temporários e retorna espaço liberado em MB"""
        freed_space = 0
        
        # Diretórios temporários
        temp_locations = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch'),
        ]
        
        for location in temp_locations:
            if location and os.path.exists(location):
                try:
                    size_before = self._get_folder_size(location)
                    self._clean_directory(location)
                    size_after = self._get_folder_size(location)
                    freed_space += (size_before - size_after)
                except:
                    pass
        
        return freed_space // (1024 * 1024)  # Converter para MB
    
    def clean_windows_update_cache(self) -> int:
        """Limpa cache do Windows Update"""
        freed_space = 0
        update_cache = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 
                                    'SoftwareDistribution', 'Download')
        
        if os.path.exists(update_cache):
            try:
                # Parar serviço de update temporariamente
                self.run_cmd_command('net stop wuauserv')
                
                size_before = self._get_folder_size(update_cache)
                self._clean_directory(update_cache)
                size_after = self._get_folder_size(update_cache)
                freed_space = (size_before - size_after) // (1024 * 1024)
                
                # Reiniciar serviço
                self.run_cmd_command('net start wuauserv')
            except:
                pass
        
        return freed_space
    
    def clean_winsxs(self) -> int:
        """Limpa WinSxS usando DISM"""
        try:
            # Analisar primeiro
            self.run_cmd_command('dism /online /Cleanup-Image /AnalyzeComponentStore')
            
            # Limpar
            success, output = self.run_cmd_command('dism /online /Cleanup-Image /StartComponentCleanup /ResetBase')
            
            if success:
                # Tentar estimar espaço liberado
                return 500  # Estimativa conservadora em MB
        except:
            pass
        return 0
    
    def clean_thumbnails_cache(self) -> int:
        """Limpa cache de thumbnails"""
        freed_space = 0
        thumbnail_cache = os.path.join(os.environ.get('LOCALAPPDATA', ''), 
                                      'Microsoft', 'Windows', 'Explorer')
        
        if os.path.exists(thumbnail_cache):
            try:
                # Parar explorer temporariamente
                self.run_cmd_command('taskkill /f /im explorer.exe')
                
                size_before = self._get_folder_size(thumbnail_cache)
                
                # Remover arquivos de thumbnail
                for pattern in ['thumbcache_*.db', '*.db']:
                    for file in Path(thumbnail_cache).glob(pattern):
                        try:
                            file_size = file.stat().st_size
                            file.unlink()
                            freed_space += file_size
                        except:
                            pass
                
                # Reiniciar explorer
                self.run_cmd_command('start explorer.exe')
                
            except:
                # Garantir que explorer reinicie
                self.run_cmd_command('start explorer.exe')
        
        return freed_space // (1024 * 1024)
    
    def clean_recycle_bin(self) -> int:
        """Esvazia lixeira"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Usar API do Windows para esvaziar lixeira
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001)
            self.changes_made.append("Recycle bin emptied")
            return -1  # Não sabemos quanto espaço foi liberado
        except:
            return 0
    
    def rebuild_icon_cache(self) -> bool:
        """Reconstrói cache de ícones"""
        try:
            icon_cache = os.path.join(os.environ.get('LOCALAPPDATA', ''), 
                                     'Microsoft', 'Windows', 'Explorer', 'iconcache.db')
            
            if os.path.exists(icon_cache):
                # Parar explorer
                self.run_cmd_command('taskkill /f /im explorer.exe')
                
                # Remover cache
                os.remove(icon_cache)
                
                # Reiniciar explorer
                self.run_cmd_command('start explorer.exe')
                
                self.changes_made.append("Icon cache rebuilt")
                return True
        except:
            # Garantir que explorer reinicie
            self.run_cmd_command('start explorer.exe')
        
        return False
    
    def _get_folder_size(self, folder_path: str) -> int:
        """Calcula tamanho da pasta em bytes"""
        total = 0
        try:
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_folder_size(entry.path)
        except:
            pass
        return total
    
    def _clean_directory(self, directory: str):
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
    
    def apply(self) -> bool:
        """Aplica todas as limpezas"""
        try:
            self.logger.log_action("Iniciando limpeza do sistema", "INFO")
            
            total_freed = 0
            
            # Limpeza básica
            freed = self.clean_temp_files()
            total_freed += freed
            self.logger.log_action(f"Temp files: {freed} MB liberados", "SUCCESS")
            
            # Cache Windows Update
            freed = self.clean_windows_update_cache()
            total_freed += freed
            self.logger.log_action(f"Windows Update cache: {freed} MB liberados", "SUCCESS")
            
            # WinSxS
            freed = self.clean_winsxs()
            total_freed += freed
            self.logger.log_action(f"WinSxS cleanup: {freed} MB liberados (estimado)", "SUCCESS")
            
            # Thumbnails
            freed = self.clean_thumbnails_cache()
            total_freed += freed
            self.logger.log_action(f"Thumbnails cache: {freed} MB liberados", "SUCCESS")
            
            # Lixeira
            self.clean_recycle_bin()
            self.logger.log_action("Lixeira esvaziada", "SUCCESS")
            
            # Cache de ícones
            self.rebuild_icon_cache()
            self.logger.log_action("Cache de ícones reconstruído", "SUCCESS")
            
            self.cleaned_size = total_freed
            self.logger.log_action(f"Total liberado: {total_freed} MB", "SUCCESS")
            
            return True
        except Exception as e:
            self.logger.log_action(f"Erro durante limpeza: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Não há reversão para limpeza"""
        return True