# modules/system_optimizer.py
import winreg
import subprocess
from typing import Dict, List
from .base_optimizer import BaseOptimizer

class SystemOptimizer(BaseOptimizer):
    """Otimiza configurações do sistema Windows"""
    
    def __init__(self):
        super().__init__()
        
    def adjust_visual_effects(self) -> bool:
        """Ajusta efeitos visuais para melhor desempenho"""
        try:
            # Chave para efeitos visuais
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            self.set_registry_value(key_path, "VisualFXSetting", 2, winreg.HKEY_CURRENT_USER)
            
            # Desativar animações
            key_path = r"Control Panel\Desktop"
            self.set_registry_value(key_path, "UserPreferencesMask", 
                                   bytes([144, 30, 3, 128, 16, 0, 0, 0]), 
                                   winreg.HKEY_CURRENT_USER, winreg.REG_BINARY)
            
            self.changes_made.append("Visual effects adjusted for performance")
            return True
        except Exception as e:
            self.errors.append(f"Erro ajuste visual: {str(e)}")
            return False
    
    def disable_transparency(self) -> bool:
        """Desativa transparência do Windows"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            self.set_registry_value(key_path, "EnableTransparency", 0, winreg.HKEY_CURRENT_USER)
            self.changes_made.append("Transparency disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro transparência: {str(e)}")
            return False
    
    def disable_background_apps(self) -> bool:
        """Desativa aplicativos em segundo plano"""
        try:
            # Desativar para todos os usuários
            key_path = r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
            self.set_registry_value(key_path, "GlobalUserDisabled", 1, winreg.HKEY_CURRENT_USER)
            
            # Desativar apps específicos
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
            self.set_registry_value(key_path, "BackgroundAppGlobalToggle", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Background apps disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro background apps: {str(e)}")
            return False
    
    def disable_notifications(self) -> bool:
        """Desativa notificações e dicas do Windows"""
        try:
            # Desativar notificações
            key_path = r"Software\Microsoft\Windows\CurrentVersion\PushNotifications"
            self.set_registry_value(key_path, "ToastEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            # Desativar dicas e sugestões
            key_path = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
            self.set_registry_value(key_path, "SubscribedContent-338387Enabled", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "SoftLandingEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Notifications and tips disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro notificações: {str(e)}")
            return False
    
    def disable_start_suggestions(self) -> bool:
        """Desativa sugestões do menu Iniciar"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
            self.set_registry_value(key_path, "SubscribedContent-338388Enabled", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "SystemPaneSuggestionsEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Start menu suggestions disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro sugestões start: {str(e)}")
            return False
    
    def disable_spotlight(self) -> bool:
        """Desativa Windows Spotlight"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
            self.set_registry_value(key_path, "RotatingLockScreenEnabled", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "RotatingLockScreenOverlayEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Windows Spotlight disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro spotlight: {str(e)}")
            return False
    
    def disable_xbox_game_bar(self) -> bool:
        """Desativa Xbox Game Bar"""
        try:
            # Desabilitar Game DVR
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR"
            self.set_registry_value(key_path, "AppCaptureEnabled", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "HistoricalCaptureEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            # Desabilitar Game Bar
            key_path = r"SOFTWARE\Microsoft\GameBar"
            self.set_registry_value(key_path, "AllowAutoGameMode", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "UseNexusForGameBarEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Xbox Game Bar disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro Xbox Game Bar: {str(e)}")
            return False
    
    def disable_auto_game_capture(self) -> bool:
        """Desativa captura automática de jogos"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR"
            self.set_registry_value(key_path, "HistoricalCaptureEnabled", 0, winreg.HKEY_CURRENT_USER)
            self.set_registry_value(key_path, "AutoCaptureEnabled", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Auto game capture disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro auto capture: {str(e)}")
            return False
    
    def disable_onedrive_sync(self) -> bool:
        """Desativa sincronização automática do OneDrive"""
        try:
            # Desabilitar inicialização automática do OneDrive
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            self.set_registry_value(key_path, "OneDrive", "", winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
            
            # Parar OneDrive se estiver rodando
            subprocess.run(['taskkill', '/f', '/im', 'OneDrive.exe'], capture_output=True)
            
            self.changes_made.append("OneDrive sync disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro OneDrive: {str(e)}")
            return False
    
    def disable_widgets(self) -> bool:
        """Desativa Widgets do Windows 11"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            self.set_registry_value(key_path, "TaskbarDa", 0, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Windows Widgets disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro widgets: {str(e)}")
            return False
    
    def disable_copilot(self) -> bool:
        """Desativa Copilot (Windows 11)"""
        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot"
            self.set_registry_value(key_path, "TurnOffWindowsCopilot", 1, winreg.HKEY_LOCAL_MACHINE)
            
            self.changes_made.append("Copilot disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro Copilot: {str(e)}")
            return False
    
    def disable_activity_history(self) -> bool:
        """Desativa histórico de atividades"""
        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\System"
            self.set_registry_value(key_path, "EnableActivityFeed", 0, winreg.HKEY_LOCAL_MACHINE)
            self.set_registry_value(key_path, "PublishUserActivities", 0, winreg.HKEY_LOCAL_MACHINE)
            self.set_registry_value(key_path, "UploadUserActivities", 0, winreg.HKEY_LOCAL_MACHINE)
            
            self.changes_made.append("Activity history disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro activity history: {str(e)}")
            return False
    
    def adjust_wait_to_kill(self) -> bool:
        """Ajusta WaitToKillServiceTimeout para encerramento mais rápido"""
        try:
            key_path = r"Control Panel\Desktop"
            self.set_registry_value(key_path, "WaitToKillServiceTimeout", "2000", 
                                   winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
            self.set_registry_value(key_path, "HungAppTimeout", "2000", 
                                   winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
            self.set_registry_value(key_path, "WaitToKillAppTimeout", "5000", 
                                   winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
            
            self.changes_made.append("WaitToKill timeout adjusted")
            return True
        except Exception as e:
            self.errors.append(f"Erro timeout: {str(e)}")
            return False
    
    def adjust_menu_delay(self) -> bool:
        """Ajusta MenuShowDelay para menus mais rápidos"""
        try:
            key_path = r"Control Panel\Desktop"
            self.set_registry_value(key_path, "MenuShowDelay", "100", 
                                   winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
            
            self.changes_made.append("Menu delay adjusted")
            return True
        except Exception as e:
            self.errors.append(f"Erro menu delay: {str(e)}")
            return False
    
    def disable_error_reporting(self) -> bool:
        """Desativa relatórios de erro automáticos"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\Windows Error Reporting"
            self.set_registry_value(key_path, "Disabled", 1, winreg.HKEY_LOCAL_MACHINE)
            
            self.changes_made.append("Error reporting disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro error reporting: {str(e)}")
            return False
    
    def disable_settings_sync(self) -> bool:
        """Desativa sincronização de configurações entre dispositivos"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync"
            self.set_registry_value(key_path, "SyncPolicy", 1, winreg.HKEY_CURRENT_USER)
            
            self.changes_made.append("Settings sync disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro settings sync: {str(e)}")
            return False
    
    def disable_fast_startup(self) -> bool:
        """Desativa inicialização rápida"""
        try:
            # Desabilitar hibernação (necessário para fast startup)
            subprocess.run(['powercfg', '/h', 'off'], capture_output=True)
            
            key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Power"
            self.set_registry_value(key_path, "HiberbootEnabled", 0, winreg.HKEY_LOCAL_MACHINE)
            
            self.changes_made.append("Fast startup disabled")
            return True
        except Exception as e:
            self.errors.append(f"Erro fast startup: {str(e)}")
            return False
    
    def disable_indexing(self, drive: str = "C:") -> bool:
        """Desativa indexação em um drive específico"""
        try:
            # Verificar se é HDD antes de desativar indexação
            disk_type = self.get_disk_type(drive)
            
            if disk_type == "HDD" or disk_type == "Desconhecido":
                # Desativar serviço de indexação
                self.enable_disable_service("WSearch", enable=False)
                
                # Desativar indexação no drive específico
                command = f'powershell -Command "Disable-MMAgent -MemoryCompression"'
                subprocess.run(command, capture_output=True, shell=True)
                
                self.changes_made.append(f"Indexing disabled on {drive}")
                return True
            else:
                self.logger.log_action(f"Indexação mantida em {drive} (SSD detectado)", "INFO")
                return False
        except Exception as e:
            self.errors.append(f"Erro indexação: {str(e)}")
            return False
    
    def apply(self) -> bool:
        """Aplica todas as otimizações do sistema"""
        try:
            self.logger.log_action("Iniciando otimizações do sistema", "INFO")
            
            # Aplicar cada otimização
            optimizations = [
                ("Efeitos visuais", self.adjust_visual_effects),
                ("Transparência", self.disable_transparency),
                ("Background apps", self.disable_background_apps),
                ("Notificações", self.disable_notifications),
                ("Sugestões Start", self.disable_start_suggestions),
                ("Spotlight", self.disable_spotlight),
                ("Xbox Game Bar", self.disable_xbox_game_bar),
                ("Auto game capture", self.disable_auto_game_capture),
                ("Widgets", self.disable_widgets),
                ("Copilot", self.disable_copilot),
                ("Histórico atividades", self.disable_activity_history),
                ("WaitToKill timeout", self.adjust_wait_to_kill),
                ("Menu delay", self.adjust_menu_delay),
                ("Error reporting", self.disable_error_reporting),
                ("Settings sync", self.disable_settings_sync),
            ]
            
            for name, func in optimizations:
                if func():
                    self.logger.log_action(f"✅ {name} otimizado", "SUCCESS")
                else:
                    self.logger.log_action(f"⚠️ {name} falhou", "WARNING")
            
            return True
        except Exception as e:
            self.logger.log_action(f"Erro otimizações sistema: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Reverte alterações do sistema"""
        return self.backup_manager.restore_all()