# modules/backup_manager.py
import json
import winreg
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class BackupManager:
    """Gerencia backups de configurações do sistema"""
    
    def __init__(self):
        self.backup_dir = Path.home() / 'WindowsOptimizer_Backups'
        self.backup_dir.mkdir(exist_ok=True)
        self.current_backup = None
        self.registry_backups = {}
        
    def backup_registry_key(self, key_path: str, value_name: str = None) -> bool:
        """Faz backup de uma chave/valor do registro"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'key_path': key_path,
                'value_name': value_name,
                'backup_type': 'registry'
            }
            
            # Tentar obter valor atual
            try:
                # Tentar abrir em HKEY_LOCAL_MACHINE primeiro
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                    hive = 'HKLM'
                except:
                    # Tentar HKEY_CURRENT_USER
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                    hive = 'HKCU'
                
                if value_name:
                    try:
                        value, value_type = winreg.QueryValueEx(key, value_name)
                        backup_data['value'] = value
                        backup_data['value_type'] = value_type
                        backup_data['hive'] = hive
                    except:
                        pass
                
                winreg.CloseKey(key)
            except:
                # Chave não existe, backup vazio
                backup_data['value'] = None
                backup_data['hive'] = 'Unknown'
            
            # Salvar backup
            backup_file = self.backup_dir / f"registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            # Registrar backup
            backup_key = f"{hive}\\{key_path}\\{value_name if value_name else ''}"
            self.registry_backups[backup_key] = backup_file
            
            return True
        except Exception as e:
            print(f"Erro backup registro: {e}")
            return False
    
    def restore_registry_key(self, backup_file: Path) -> bool:
        """Restaura uma chave de registro do backup"""
        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            if backup_data.get('value') is not None:
                hive = winreg.HKEY_LOCAL_MACHINE if backup_data.get('hive') == 'HKLM' else winreg.HKEY_CURRENT_USER
                
                # Abrir ou criar chave
                try:
                    key = winreg.OpenKey(hive, backup_data['key_path'], 0, winreg.KEY_SET_VALUE)
                except:
                    key = winreg.CreateKey(hive, backup_data['key_path'])
                
                # Restaurar valor
                if backup_data.get('value_name'):
                    winreg.SetValueEx(
                        key,
                        backup_data['value_name'],
                        0,
                        backup_data.get('value_type', winreg.REG_DWORD),
                        backup_data['value']
                    )
                
                winreg.CloseKey(key)
            
            return True
        except Exception as e:
            print(f"Erro restore registro: {e}")
            return False
    
    def restore_all(self) -> bool:
        """Restaura todos os backups"""
        success = True
        for backup_file in self.registry_backups.values():
            if not self.restore_registry_key(Path(backup_file)):
                success = False
        return success
    
    def clear_old_backups(self, days: int = 7):
        """Limpa backups mais antigos que X dias"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        for backup_file in self.backup_dir.glob('*.json'):
            if backup_file.stat().st_mtime < cutoff:
                try:
                    backup_file.unlink()
                except:
                    pass