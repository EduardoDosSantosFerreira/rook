# modules/power_optimizer.py
import subprocess
import winreg

class PowerOptimizer:
    """Otimiza configurações de energia do Windows"""
    
    def apply_optimizations(self):
        """Aplica todas as otimizações de energia"""
        try:
            # Desativar hibernação
            subprocess.run(['powercfg', '/hibernate', 'off'], 
                         capture_output=True, shell=True)
            
            # Ativar plano Ultimate Performance
            subprocess.run(['powercfg', '-duplicatescheme', 
                          'e9a42b02-d5df-448d-aa00-03f14749eb61'], 
                         capture_output=True, shell=True)
            
            # Ajustar configurações do processador
            self._optimize_processor_settings()
            
            return True
        except Exception as e:
            print(f"Erro nas otimizações de energia: {e}")
            return False
            
    def _optimize_processor_settings(self):
        """Ajusta configurações do processador para melhor performance"""
        try:
            # Priorizar desempenho do processador
            subprocess.run(['powercfg', '-setacvalueindex', 
                          'SCHEME_CURRENT', 'SUB_PROCESSOR', 
                          'PERFINCPOL', '2'], capture_output=True, shell=True)
            subprocess.run(['powercfg', '-setactive', 'SCHEME_CURRENT'], 
                         capture_output=True, shell=True)
        except:
            pass