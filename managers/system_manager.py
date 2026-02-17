# managers/system_manager.py
import psutil
import platform
from datetime import datetime

class SystemManager:
    """Gerenciador de informações do sistema"""
    
    def __init__(self):
        self.system_info = {}
        self.update_system_info()
        
    def update_system_info(self):
        """Atualiza informações do sistema"""
        try:
            self.system_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': psutil.disk_usage('C:')._asdict(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Erro ao atualizar informações: {e}")
            
    def get_cpu_usage(self):
        """Retorna uso da CPU"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except:
            return 0
            
    def get_memory_usage(self):
        """Retorna uso da memória"""
        try:
            memory = psutil.virtual_memory()
            return {
                'percent': memory.percent,
                'used': memory.used,
                'total': memory.total
            }
        except:
            return {'percent': 0, 'used': 0, 'total': 0}
            
    def get_disk_usage(self, path='C:'):
        """Retorna uso do disco"""
        try:
            disk = psutil.disk_usage(path)
            return {
                'percent': disk.percent,
                'used': disk.used,
                'total': disk.total,
                'free': disk.free
            }
        except:
            return {'percent': 0, 'used': 0, 'total': 0, 'free': 0}