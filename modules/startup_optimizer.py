# modules/startup_optimizer.py
import os
import winreg
from pathlib import Path
from typing import List, Dict
from .base_optimizer import BaseOptimizer

class StartupOptimizer(BaseOptimizer):
    """Gerencia programas que iniciam com o Windows"""
    
    def __init__(self):
        super().__init__()
        self.startup_locations = {
            "HKCU_Run": (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            "HKLM_Run": (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            "HKCU_RunOnce": (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            "HKLM_RunOnce": (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            "Startup_Folder": Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        }
        
        self.safe_to_disable = [
            "OneDrive",
            "Adobe Reader",
            "QuickTime",
            "iTunes",
            "Spotify",
            "Discord",
            "Steam",
            "EpicGamesLauncher",
            "Battle.net",
            "Origin",
            "Skype",
            "Teams",
            "Zoom",
            "Slack",
            "Telegram",
            "WhatsApp"
        ]
        
    def get_startup_items(self) -> List[Dict]:
        """Lista todos os itens de inicialização"""
        items = []
        
        # Verificar registro
        for location_name, (hive, key_path) in self.startup_locations.items():
            if "Run" in location_name and "Folder" not in location_name:
                try:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            items.append({
                                "name": name,
                                "command": value,
                                "location": location_name,
                                "type": "registry"
                            })
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except:
                    pass
        
        # Verificar pasta de inicialização
        startup_folder = self.startup_locations["Startup_Folder"]
        if startup_folder.exists():
            for shortcut in startup_folder.glob("*.lnk"):
                items.append({
                    "name": shortcut.stem,
                    "path": str(shortcut),
                    "location": "Startup_Folder",
                    "type": "shortcut"
                })
        
        return items
    
    def disable_startup_item(self, item_name: str, location: str) -> bool:
        """Desabilita um item específico de inicialização"""
        try:
            if location == "Startup_Folder":
                # Mover atalho para backup
                startup_folder = self.startup_locations["Startup_Folder"]
                backup_folder = startup_folder.parent / "Startup_Backup"
                backup_folder.mkdir(exist_ok=True)
                
                shortcut_path = startup_folder / f"{item_name}.lnk"
                if shortcut_path.exists():
                    backup_path = backup_folder / f"{item_name}_disabled_{datetime.now().strftime('%Y%m%d')}.lnk"
                    shortcut_path.rename(backup_path)
                    self.changes_made.append(f"Startup shortcut disabled: {item_name}")
                    return True
            else:
                # Remover do registro
                hive, key_path = {
                    "HKCU_Run": (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                    "HKLM_Run": (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                }.get(location, (None, None))
                
                if hive and key_path:
                    # Backup antes de deletar
                    self.backup_manager.backup_registry_key(key_path, item_name)
                    
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.DeleteValue(key, item_name)
                    winreg.CloseKey(key)
                    self.changes_made.append(f"Registry startup item disabled: {item_name}")
                    return True
                    
            return False
        except Exception as e:
            self.errors.append(f"Erro desabilitando {item_name}: {str(e)}")
            return False
    
    def disable_recommended_startup(self) -> int:
        """Desabilita itens de inicialização recomendados"""
        disabled_count = 0
        items = self.get_startup_items()
        
        for item in items:
            for safe_name in self.safe_to_disable:
                if safe_name.lower() in item["name"].lower():
                    if self.disable_startup_item(item["name"], item["location"]):
                        disabled_count += 1
                    break
        
        return disabled_count
    
    def apply(self) -> bool:
        """Aplica otimizações de inicialização"""
        try:
            self.logger.log_action("Iniciando otimização de inicialização", "INFO")
            
            # Desabilitar itens recomendados
            disabled = self.disable_recommended_startup()
            self.logger.log_action(f"{disabled} itens de inicialização desabilitados", "SUCCESS")
            
            # Desabilitar inicialização rápida (pode causar problemas com hibernação)
            self.set_registry_value(
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
                "HiberbootEnabled",
                0
            )
            
            return True
        except Exception as e:
            self.logger.log_action(f"Erro otimização inicialização: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Reverte alterações de inicialização"""
        return self.backup_manager.restore_all()