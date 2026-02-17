# modules/base_optimizer.py
import subprocess
import winreg
import ctypes
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .logger import Logger
from .backup_manager import BackupManager

class BaseOptimizer(ABC):
    """Classe base para todos os otimizadores"""
    
    def __init__(self):
        self.logger = Logger()
        self.backup_manager = BackupManager()
        self.changes_made = []
        self.errors = []
        
    @abstractmethod
    def apply(self) -> bool:
        """Aplica as otimizações - deve ser implementado por cada módulo"""
        pass
    
    @abstractmethod
    def revert(self) -> bool:
        """Reverte as alterações - deve ser implementado por cada módulo"""
        pass
    
    def run_powershell_command(self, command: str, as_admin: bool = True) -> Tuple[bool, str]:
        """Executa comando PowerShell e retorna (sucesso, saída)"""
        try:
            full_command = f'powershell -Command "{command}"'
            result = subprocess.run(full_command, capture_output=True, text=True, shell=True)
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            return success, output
        except Exception as e:
            self.errors.append(f"Erro PowerShell: {str(e)}")
            return False, str(e)
    
    def run_cmd_command(self, command: str) -> Tuple[bool, str]:
        """Executa comando CMD e retorna (sucesso, saída)"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            return success, output
        except Exception as e:
            self.errors.append(f"Erro CMD: {str(e)}")
            return False, str(e)
    
    def set_registry_value(self, key_path: str, value_name: str, value_data, 
                          hive=winreg.HKEY_LOCAL_MACHINE, value_type=winreg.REG_DWORD):
        """Define valor no registro com backup automático"""
        try:
            # Fazer backup antes de modificar
            self.backup_manager.backup_registry_key(key_path, value_name)
            
            # Abrir ou criar chave
            try:
                key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
            except FileNotFoundError:
                key = winreg.CreateKey(hive, key_path)
            
            # Definir valor
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
            winreg.CloseKey(key)
            
            self.changes_made.append(f"Registro: {key_path}\\{value_name} = {value_data}")
            return True
        except Exception as e:
            self.errors.append(f"Erro registro {key_path}: {str(e)}")
            return False
    
    def get_registry_value(self, key_path: str, value_name: str, 
                          hive=winreg.HKEY_LOCAL_MACHINE, default=None):
        """Obtém valor do registro"""
        try:
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return value
        except:
            return default
    
    def enable_disable_service(self, service_name: str, enable: bool = False) -> bool:
        """Habilita ou desabilita um serviço do Windows"""
        try:
            action = "enable" if enable else "disable"
            success, output = self.run_cmd_command(f'sc config {service_name} start= {action}')
            
            if not enable:  # Se desabilitando, para o serviço se estiver rodando
                self.run_cmd_command(f'net stop {service_name} /y')
            
            return success
        except Exception as e:
            self.errors.append(f"Erro serviço {service_name}: {str(e)}")
            return False
    
    def get_disk_type(self, drive: str = "C:") -> str:
        """Detecta se o disco é HDD ou SSD"""
        try:
            # Usando PowerShell para detectar tipo de mídia
            command = f'Get-PhysicalDisk | Where-Object {{$_.DeviceID -eq (Get-Partition -DriveLetter {drive[0]} | Get-Disk).Number}} | Select-Object -ExpandProperty MediaType'
            success, output = self.run_powershell_command(command)
            
            if success and output:
                media_type = output.strip()
                if "SSD" in media_type:
                    return "SSD"
                elif "HDD" in media_type:
                    return "HDD"
            return "Desconhecido"
        except:
            return "Desconhecido"
    
    def get_disk_usage(self, drive: str = "C:") -> float:
        """Obtém porcentagem de uso do disco"""
        try:
            usage = ctypes.c_ulonglong()
            total = ctypes.c_ulonglong()
            free = ctypes.c_ulonglong()
            
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(drive),
                ctypes.byref(usage),
                ctypes.byref(total),
                ctypes.byref(free)
            )
            
            used_percent = ((total.value - free.value) / total.value) * 100
            return used_percent
        except:
            return 0.0
    
    def get_summary(self) -> Dict:
        """Retorna resumo das operações"""
        return {
            "changes_made": self.changes_made,
            "errors": self.errors,
            "success_count": len(self.changes_made),
            "error_count": len(self.errors)
        }