# modules/restore_manager.py
import subprocess
import winreg
from datetime import datetime
from .base_optimizer import BaseOptimizer

class RestoreManager(BaseOptimizer):
    """Gerencia pontos de restauração do sistema"""
    
    def __init__(self):
        super().__init__()
        self.restore_point_name = None
        
    def create_restore_point(self, description: str = None) -> bool:
        """Cria um ponto de restauração do sistema"""
        try:
            if not description:
                description = f"WindowsOptimizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.restore_point_name = description
            
            # Habilitar proteção do sistema no drive C: se necessário
            subprocess.run([
                'powershell', '-Command',
                'Enable-ComputerRestore -Drive "C:\\"'
            ], capture_output=True)
            
            # Criar ponto de restauração
            result = subprocess.run([
                'powershell', '-Command',
                f'Checkpoint-Computer -Description "{description}" -RestorePointType MODIFY_SETTINGS'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.log_action(f"Ponto de restauração criado: {description}", "SUCCESS")
                return True
            else:
                self.logger.log_action(f"Falha ao criar ponto de restauração: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.logger.log_action(f"Erro ao criar ponto de restauração: {str(e)}", "ERROR")
            return False
    
    def list_restore_points(self) -> list:
        """Lista pontos de restauração existentes"""
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-ComputerRestorePoint | Select-Object Description,CreationTime,SequenceNumber | ConvertTo-Json'
            ], capture_output=True, text=True)
            
            import json
            if result.stdout.strip():
                return json.loads(result.stdout)
            return []
        except:
            return []
    
    def restore_to_point(self, sequence_number: int) -> bool:
        """Restaura sistema para um ponto específico"""
        try:
            result = subprocess.run([
                'powershell', '-Command',
                f'Restore-Computer -RestorePoint {sequence_number} -Confirm:$false'
            ], capture_output=True)
            
            return result.returncode == 0
        except:
            return False
    
    def apply(self) -> bool:
        """Cria ponto de restauração"""
        return self.create_restore_point()
    
    def revert(self) -> bool:
        """Reverte para o último ponto de restauração"""
        points = self.list_restore_points()
        if points and len(points) > 0:
            # Encontrar nosso ponto mais recente
            for point in points:
                if point.get('Description', '').startswith('WindowsOptimizer'):
                    return self.restore_to_point(point.get('SequenceNumber'))
        return False