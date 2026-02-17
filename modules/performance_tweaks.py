# modules/performance_tweaks.py
import subprocess
import winreg

class PerformanceTweaks:
    """Aplica ajustes de desempenho ao Windows"""
    
    def apply_tweaks(self):
        """Aplica todos os ajustes de desempenho"""
        try:
            # Ajustar efeitos visuais para melhor desempenho
            self._adjust_visual_effects()
            
            # Priorizar programas no agendamento do processador
            self._prioritize_programs()
            
            return True
        except Exception as e:
            print(f"Erro nos ajustes de desempenho: {e}")
            return False
            
    def _adjust_visual_effects(self):
        """Ajusta efeitos visuais para melhor desempenho"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
        except:
            pass
            
    def _prioritize_programs(self):
        """Prioriza programas no agendamento do processador"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"System\CurrentControlSet\Control\PriorityControl",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 38)
            winreg.CloseKey(key)
        except:
            pass