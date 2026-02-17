# modules/diagnostics.py
import subprocess
import psutil
import wmi
from typing import Dict, List
from .base_optimizer import BaseOptimizer

class Diagnostics(BaseOptimizer):
    """Módulo de diagnóstico e monitoramento"""
    
    def __init__(self):
        super().__init__()
        self.wmi_conn = wmi.WMI()
        
    def check_disk_health(self) -> Dict:
        """Verifica saúde dos discos"""
        health_info = {}
        
        for disk in self.wmi_conn.Win32_DiskDrive():
            health_info[disk.Model] = {
                "status": disk.Status,
                "size_gb": int(disk.Size) // (1024**3) if disk.Size else 0,
                "interface": disk.InterfaceType,
                "media_type": self.get_disk_type(disk.DeviceID[:2])
            }
            
            # Alertar se SSD estiver muito cheio
            if health_info[disk.Model]["media_type"] == "SSD":
                usage = self.get_disk_usage(disk.DeviceID[:2])
                if usage > 85:
                    self.logger.log_action(
                        f"⚠️ ALERTA: {disk.Model} está com {usage:.1f}% de uso!",
                        "WARNING"
                    )
        
        return health_info
    
    def scan_system_files(self) -> bool:
        """Executa SFC /scannow"""
        try:
            self.logger.log_action("Executando SFC /scannow...", "INFO")
            success, output = self.run_cmd_command('sfc /scannow')
            
            if "Windows Resource Protection did not find any integrity violations" in output:
                self.logger.log_action("✅ SFC: Sistema íntegro", "SUCCESS")
            elif "Windows Resource Protection found corrupt files and successfully repaired them" in output:
                self.logger.log_action("✅ SFC: Arquivos reparados", "SUCCESS")
            else:
                self.logger.log_action("⚠️ SFC: Verificação concluída com avisos", "WARNING")
            
            return success
        except Exception as e:
            self.logger.log_action(f"Erro SFC: {str(e)}", "ERROR")
            return False
    
    def scan_dism(self) -> bool:
        """Executa DISM /RestoreHealth"""
        try:
            self.logger.log_action("Executando DISM /RestoreHealth...", "INFO")
            success, output = self.run_cmd_command('dism /online /cleanup-image /restorehealth')
            
            if "The restore operation completed successfully" in output:
                self.logger.log_action("✅ DISM: Imagem restaurada", "SUCCESS")
            else:
                self.logger.log_action("⚠️ DISM: Verificação concluída", "WARNING")
            
            return success
        except Exception as e:
            self.logger.log_action(f"Erro DISM: {str(e)}", "ERROR")
            return False
    
    def check_disk_integrity(self, drive: str = "C:") -> bool:
        """Executa CHKDSK no drive especificado"""
        try:
            # Primeiro verificar sem reparar
            success, output = self.run_cmd_command(f'chkdsk {drive} /scan')
            
            if "Windows has scanned the file system and found no problems" in output:
                self.logger.log_action(f"✅ CHKDSK {drive}: Sistema íntegro", "SUCCESS")
                return True
            else:
                # Perguntar se quer reparar
                self.logger.log_action(
                    f"⚠️ CHKDSK {drive}: Problemas detectados. Execute com /f para reparar",
                    "WARNING"
                )
                return False
        except Exception as e:
            self.logger.log_action(f"Erro CHKDSK: {str(e)}", "ERROR")
            return False
    
    def find_high_cpu_drivers(self) -> List[str]:
        """Detecta drivers com alto consumo de CPU"""
        high_cpu_drivers = []
        
        try:
            # Usar WMI para monitorar processos do sistema
            for process in self.wmi_conn.Win32_Process():
                if process.Name and process.KernelModeTime and process.UserModeTime:
                    cpu_time = int(process.KernelModeTime) + int(process.UserModeTime)
                    # Drivers geralmente são .sys
                    if process.Name.endswith('.sys') and cpu_time > 10000000:  # Alto consumo
                        high_cpu_drivers.append(process.Name)
        except:
            pass
        
        return high_cpu_drivers
    
    def clear_standby_memory(self) -> bool:
        """Limpa memória standby (uso controlado)"""
        try:
            # Usar PowerShell para limpar standby list
            command = """
            [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices")
            $size = [System.Runtime.InteropServices.Marshal]::SizeOf([type][System.UInt64])
            $start = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($size)
            [System.Runtime.InteropServices.Marshal]::WriteInt64($start, 0xffffffffffffffff)
            [System.Runtime.InteropServices.Marshal]::WriteInt64([System.IntPtr]::Add($start, $size), 0x0)
            [Microsoft.Win32.NativeMethods]::NtSetSystemInformation(
                "MemoryStandbyInformation",
                $start,
                [System.UInt32](2 * $size)
            )
            """
            
            success, _ = self.run_powershell_command(command)
            
            if success:
                self.logger.log_action("✅ Memória standby limpa", "SUCCESS")
                return True
        except:
            pass
        
        return False
    
    def get_system_info(self) -> Dict:
        """Obtém informações detalhadas do sistema"""
        info = {}
        
        try:
            # CPU
            info['cpu'] = {
                'name': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
                'cores': psutil.cpu_count(),
                'usage': psutil.cpu_percent(interval=1)
            }
            
            # Memória
            memory = psutil.virtual_memory()
            info['memory'] = {
                'total_gb': memory.total / (1024**3),
                'available_gb': memory.available / (1024**3),
                'usage_percent': memory.percent
            }
            
            # Discos
            info['disks'] = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info['disks'].append({
                        'mount': partition.mountpoint,
                        'total_gb': usage.total / (1024**3),
                        'used_gb': usage.used / (1024**3),
                        'free_gb': usage.free / (1024**3),
                        'usage_percent': usage.percent,
                        'type': self.get_disk_type(partition.mountpoint)
                    })
                except:
                    continue
        except:
            pass
        
        return info
    
    def apply(self) -> bool:
        """Executa diagnósticos"""
        try:
            self.logger.log_action("Iniciando diagnósticos do sistema", "INFO")
            
            # Verificar saúde dos discos
            disk_health = self.check_disk_health()
            self.logger.log_action(f"✅ {len(disk_health)} discos verificados", "SUCCESS")
            
            # Verificar drivers com alto consumo
            high_cpu = self.find_high_cpu_drivers()
            if high_cpu:
                self.logger.log_action(f"⚠️ Drivers com alto consumo: {', '.join(high_cpu)}", "WARNING")
            
            # Informações do sistema
            sys_info = self.get_system_info()
            self.logger.log_action(
                f"📊 CPU: {sys_info['cpu']['usage']}% | RAM: {sys_info['memory']['usage_percent']:.1f}%",
                "INFO"
            )
            
            return True
        except Exception as e:
            self.logger.log_action(f"Erro diagnósticos: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Não há reversão para diagnósticos"""
        return True