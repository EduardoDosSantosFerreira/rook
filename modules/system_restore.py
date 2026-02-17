# modules/system_restore.py
import subprocess
import ctypes
from datetime import datetime

class SystemRestore:
    """Gerencia pontos de restauração do sistema"""
    
    def __init__(self):
        self.restore_point_name = f"WindowsOptimizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_restore_point(self):
        """Cria um ponto de restauração do sistema"""
        try:
            # Verificar se o serviço de restauração está ativo
            subprocess.run(['powershell', '-Command', 
                'Enable-ComputerRestore -Drive "C:\\"'], 
                capture_output=True, shell=True)
            
            # Criar ponto de restauração
            result = subprocess.run(['powershell', '-Command',
                f'Checkpoint-Computer -Description "{self.restore_point_name}" -RestorePointType MODIFY_SETTINGS'],
                capture_output=True, shell=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao criar ponto de restauração: {e}")
            return False