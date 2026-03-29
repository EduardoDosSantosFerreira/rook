# core/optimizer.py
"""
Módulo principal de otimização - Contém todas as funcionalidades
"""
import subprocess
import winreg
import ctypes
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Tuple


class Optimizer:
    """Gerencia todas as otimizações do sistema"""
    
    def __init__(self, logger):
        self.logger = logger
        self.changes = []
    
    def create_restore_point(self) -> bool:
        """Cria ponto de restauração do sistema"""
        try:
            self.logger.info("Criando ponto de restauração...")
            
            # Habilitar proteção no drive C:
            subprocess.run([
                'powershell', '-Command',
                'Enable-ComputerRestore -Drive "C:\\"'
            ], capture_output=True)
            
            # Criar ponto de restauração
            result = subprocess.run([
                'powershell', '-Command',
                'Checkpoint-Computer -Description "rook_optimizer" -RestorePointType MODIFY_SETTINGS'
            ], capture_output=True)
            
            if result.returncode == 0:
                self.logger.success("Ponto de restauração criado")
                self.changes.append("Ponto de restauração criado")
                return True
            else:
                self.logger.warning("Falha ao criar ponto de restauração")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao criar ponto de restauração: {e}")
            return False
    
    def adjust_visual_effects(self) -> bool:
        """Ajusta efeitos visuais para máximo desempenho"""
        try:
            self.logger.info("Ajustando efeitos visuais...")
            
            # Configurar para melhor desempenho
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_path, 0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            # Desativar transparência
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, key_path, 0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
            except:
                pass
            
            self.logger.success("Efeitos visuais ajustados para desempenho")
            self.changes.append("Efeitos visuais otimizados")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao ajustar efeitos visuais: {e}")
            return False
    
    def disable_hibernation(self) -> bool:
        """Desativa hibernação para liberar espaço em disco"""
        try:
            self.logger.info("Desativando hibernação...")
            
            result = subprocess.run(
                ['powercfg', '/hibernate', 'off'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.logger.success("Hibernação desativada")
                self.changes.append("Hibernação desativada")
                return True
            else:
                self.logger.warning("Falha ao desativar hibernação")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao desativar hibernação: {e}")
            return False
    
    def enable_ultimate_performance(self) -> bool:
        """Ativa plano de energia Ultimate Performance"""
        try:
            self.logger.info("Ativando plano Ultimate Performance...")
            
            # Duplicar esquema (se não existir)
            subprocess.run([
                'powercfg', '-duplicatescheme',
                'e9a42b02-d5df-448d-aa00-03f14749eb61'
            ], capture_output=True)
            
            # Ativar plano
            result = subprocess.run([
                'powercfg', '-setactive',
                'e9a42b02-d5df-448d-aa00-03f14749eb61'
            ], capture_output=True)
            
            if result.returncode == 0:
                self.logger.success("Plano Ultimate Performance ativado")
                self.changes.append("Plano de energia ativado")
                return True
            else:
                self.logger.warning("Falha ao ativar plano Ultimate Performance")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao ativar plano de energia: {e}")
            return False
    
    def stop_tracking_processes(self) -> int:
        """Interrompe processos de rastreamento"""
        try:
            self.logger.info("Interrompendo processos de rastreamento...")
            
            # Lista de processos de telemetria
            tracking_processes = [
                "CompatTelRunner.exe",
                "diagtrack.exe",
                "dmwappushsvc.exe",
                "MapsBroker.exe",
                "OneDrive.exe",
                "WmiPrvSE.exe",
            ]
            
            stopped = 0
            for proc in tracking_processes:
                try:
                    result = subprocess.run(
                        ['taskkill', '/f', '/im', proc],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        stopped += 1
                        self.logger.info(f"Processo interrompido: {proc}")
                except:
                    pass
            
            self.logger.success(f"{stopped} processos de rastreamento interrompidos")
            self.changes.append(f"{stopped} processos interrompidos")
            return stopped
            
        except Exception as e:
            self.logger.error(f"Erro ao interromper processos: {e}")
            return 0
    
    def clean_temp_files(self) -> Tuple[int, int]:
        """Limpa arquivos temporários e retorna (arquivos, MB)"""
        try:
            self.logger.info("Limpando arquivos temporários...")
            
            file_count = 0
            bytes_freed = 0
            
            # Diretórios para limpar
            temp_dirs = [
                tempfile.gettempdir(),
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in Path(temp_dir).glob('*'):
                        try:
                            if item.is_file():
                                bytes_freed += item.stat().st_size
                                item.unlink()
                                file_count += 1
                            elif item.is_dir():
                                shutil.rmtree(item, ignore_errors=True)
                        except:
                            pass
            
            # Limpar arquivos .tmp em todo sistema
            for drive in [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]:
                try:
                    for root, dirs, files in os.walk(drive):
                        for file in files:
                            if file.lower().endswith('.tmp'):
                                try:
                                    file_path = os.path.join(root, file)
                                    bytes_freed += os.path.getsize(file_path)
                                    os.remove(file_path)
                                    file_count += 1
                                except:
                                    pass
                except:
                    continue
            
            mb_freed = bytes_freed // (1024 * 1024)
            self.logger.success(f"Limpeza concluída: {file_count} arquivos, {mb_freed} MB liberados")
            self.changes.append(f"Limpeza: {mb_freed} MB liberados")
            return file_count, mb_freed
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza: {e}")
            return 0, 0
    
    def prioritize_cpu(self) -> bool:
        """Prioriza uso de CPU para aplicações em execução"""
        try:
            self.logger.info("Priorizando CPU para aplicações...")
            
            # Ajustar prioridade do processador
            key_path = r"System\CurrentControlSet\Control\PriorityControl"
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, key_path, 0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 38)
            winreg.CloseKey(key)
            
            self.logger.success("CPU priorizada para aplicações")
            self.changes.append("Priorização de CPU ativada")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao priorizar CPU: {e}")
            return False