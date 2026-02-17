# modules/__init__.py
"""
Módulos de otimização do Windows Optimizer Pro
Contém toda a lógica de negócios e otimizações do sistema
"""

from .base_optimizer import BaseOptimizer
from .startup_optimizer import StartupOptimizer
from .services_optimizer import ServicesOptimizer
from .power_optimizer import PowerOptimizer
from .cleanup_optimizer import CleanupOptimizer
from .system_optimizer import SystemOptimizer
from .network_optimizer import NetworkOptimizer
from .diagnostics import Diagnostics
from .restore_manager import RestoreManager
from .backup_manager import BackupManager
from .logger import Logger

# Configurar encoding para Windows
import sys
import os

# Forçar UTF-8 no console Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

__all__ = [
    # Classes base
    'BaseOptimizer',
    
    # Otimizadores específicos
    'StartupOptimizer',
    'ServicesOptimizer',
    'PowerOptimizer',
    'CleanupOptimizer',
    'SystemOptimizer',
    'NetworkOptimizer',
    
    # Diagnóstico e gerenciamento
    'Diagnostics',
    'RestoreManager',
    'BackupManager',
    'Logger'
]

__version__ = '2.0.0'
__author__ = 'Windows Optimizer Pro Team'

# Informações do pacote
PACKAGE_INFO = {
    'name': 'Windows Optimizer Pro Modules',
    'version': __version__,
    'description': 'Módulos de otimização para Windows',
    'modules_count': len(__all__),
    'compatible_with': ['Windows 10', 'Windows 11']
}

def get_available_modules():
    """Retorna lista de módulos disponíveis com suas descrições"""
    modules_info = {
        'StartupOptimizer': 'Gerencia programas na inicializacao',
        'ServicesOptimizer': 'Otimiza servicos do Windows',
        'PowerOptimizer': 'Configuracoes de energia e desempenho',
        'CleanupOptimizer': 'Limpeza avancada do sistema',
        'SystemOptimizer': 'Ajustes gerais do sistema',
        'NetworkOptimizer': 'Otimizacoes de rede',
        'Diagnostics': 'Diagnostico e monitoramento',
        'RestoreManager': 'Gerenciamento de pontos de restauracao',
        'BackupManager': 'Backup de configuracoes',
        'Logger': 'Sistema de logs'
    }
    
    available = {}
    for module_name in __all__:
        if module_name in modules_info:
            available[module_name] = modules_info[module_name]
    
    return available

def get_module_summary():
    """Retorna um resumo de todos os módulos carregados"""
    return {
        'total_modules': len(__all__),
        'modules': __all__,
        'version': __version__
    }

# Inicialização do módulo (sem emojis)
print(f"[INFO] Modulos do Windows Optimizer Pro v{__version__} carregados")
print(f"[INFO] {len(__all__)} modulos disponiveis")