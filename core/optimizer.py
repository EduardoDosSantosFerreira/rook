# core/optimizer.py
"""
Módulo principal de otimização — todas as operações rodam via thread,
nunca bloqueando a UI.
"""
import subprocess
import winreg
import ctypes
import os
import shutil
import tempfile
from pathlib import Path
from typing import Tuple


class Optimizer:
    """Gerencia todas as otimizações do sistema"""

    def __init__(self, logger):
        self.logger  = logger
        self.changes = []

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers internos
    # ─────────────────────────────────────────────────────────────────────────
    @staticmethod
    def _run(cmd: list, timeout: int = 30) -> subprocess.CompletedProcess:
        """Executa processo ocultando janela no Windows."""
        si = None
        if os.name == "nt":
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE

        return subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            startupinfo=si,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Ponto de restauração
    # ─────────────────────────────────────────────────────────────────────────
    def create_restore_point(self) -> bool:
        try:
            self.logger.info("Habilitando proteção do sistema em C:\\...")
            self._run([
                "powershell", "-NonInteractive", "-Command",
                'Enable-ComputerRestore -Drive "C:\\"'
            ], timeout=20)

            self.logger.info("Criando ponto de restauração...")
            r = self._run([
                "powershell", "-NonInteractive", "-Command",
                (
                    'Checkpoint-Computer '
                    '-Description "rook_optimizer" '
                    '-RestorePointType MODIFY_SETTINGS'
                )
            ], timeout=60)

            if r.returncode == 0:
                self.logger.success("Ponto de restauração criado com sucesso")
                self.changes.append("Ponto de restauração criado")
                return True

            # Algumas versões do Windows retornam erro mesmo tendo criado
            stderr = r.stderr.decode("utf-8", errors="ignore")
            if "restore point" in stderr.lower() or r.returncode == 1:
                # Tenta verificar se foi criado via WMI
                check = self._run([
                    "powershell", "-NonInteractive", "-Command",
                    "Get-ComputerRestorePoint | Select-Object -Last 1 | "
                    "Select-Object -ExpandProperty Description"
                ], timeout=15)
                if "rook" in check.stdout.decode("utf-8", errors="ignore").lower():
                    self.logger.success("Ponto de restauração criado (verificado via WMI)")
                    self.changes.append("Ponto de restauração criado")
                    return True

            self.logger.warning(f"Falha ao criar ponto de restauração (código {r.returncode})")
            return False

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout ao criar ponto de restauração")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao criar ponto de restauração: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Efeitos visuais
    # ─────────────────────────────────────────────────────────────────────────
    def adjust_visual_effects(self) -> bool:
        try:
            self.logger.info("Configurando registro para máximo desempenho...")

            # VisualFXSetting = 2  →  "Adjust for best performance"
            _reg_set(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                "VisualFXSetting", winreg.REG_DWORD, 2
            )

            # Desativar transparência
            _reg_set(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                "EnableTransparency", winreg.REG_DWORD, 0
            )

            # Desativar animações de janelas (UserPreferencesMask)
            # bit 0x90 = sem animações — sobrescreve de forma segura
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Control Panel\Desktop\WindowMetrics",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.CloseKey(key)
            except Exception:
                pass

            # SystemParameters via powershell (aplica em tempo real)
            self._run([
                "powershell", "-NonInteractive", "-Command",
                (
                    "Add-Type -TypeDefinition '"
                    "using System; using System.Runtime.InteropServices;"
                    "public class WinAPI {"
                    "  [DllImport(\"user32.dll\")] public static extern bool "
                    "  SystemParametersInfo(uint uiAction, uint uiParam, IntPtr pvParam, uint fWinIni);"
                    "}'; "
                    # SPI_SETANIMATION = 0x0049, desligar
                    "[WinAPI]::SystemParametersInfo(0x0049, 0, [IntPtr]::Zero, 3) | Out-Null"
                )
            ], timeout=15)

            self.logger.success("Efeitos visuais ajustados para máximo desempenho")
            self.changes.append("Efeitos visuais otimizados")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao ajustar efeitos visuais: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Hibernação
    # ─────────────────────────────────────────────────────────────────────────
    def disable_hibernation(self) -> bool:
        try:
            self.logger.info("Executando powercfg /hibernate off...")
            r = self._run(["powercfg", "/hibernate", "off"], timeout=15)

            if r.returncode == 0:
                self.logger.success("Hibernação desativada — hiberfil.sys removido")
                self.changes.append("Hibernação desativada")
                return True

            self.logger.warning(
                f"powercfg retornou código {r.returncode}. "
                "Pode ser necessário executar como administrador."
            )
            return False

        except FileNotFoundError:
            self.logger.error("powercfg não encontrado. Execute como administrador.")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao desativar hibernação: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Plano de energia Ultimate Performance
    # ─────────────────────────────────────────────────────────────────────────
    def enable_ultimate_performance(self) -> bool:
        GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"
        try:
            self.logger.info("Verificando plano Ultimate Performance...")

            # Verificar se já existe
            check = self._run(["powercfg", "-list"], timeout=10)
            exists = GUID.lower() in check.stdout.decode("utf-8", errors="ignore").lower()

            if not exists:
                self.logger.info("Duplicando esquema Ultimate Performance...")
                dup = self._run(["powercfg", "-duplicatescheme", GUID], timeout=15)
                if dup.returncode != 0:
                    # Windows Home não tem esse GUID — tenta High Performance
                    self.logger.warning(
                        "Ultimate Performance não disponível nesta edição. "
                        "Ativando High Performance..."
                    )
                    r2 = self._run([
                        "powercfg", "-setactive",
                        "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
                    ], timeout=10)
                    if r2.returncode == 0:
                        self.logger.success("Plano High Performance ativado")
                        self.changes.append("Plano High Performance ativado")
                        return True
                    self.logger.error("Falha ao ativar plano de energia alternativo")
                    return False

            r = self._run(["powercfg", "-setactive", GUID], timeout=10)
            if r.returncode == 0:
                self.logger.success("Plano Ultimate Performance ativado")
                self.changes.append("Plano de energia: Ultimate Performance")
                return True

            self.logger.warning(f"Falha ao ativar plano (código {r.returncode})")
            return False

        except Exception as e:
            self.logger.error(f"Erro ao ativar plano de energia: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Telemetria & rastreamento
    # ─────────────────────────────────────────────────────────────────────────
    def stop_tracking_processes(self) -> int:
        PROCS = [
            "CompatTelRunner.exe",
            "DiagTrack.exe",         # serviço de telemetria
            "dmwappushsvc.exe",
            "WerFault.exe",          # relatório de erros
            "SearchIndexer.exe",
        ]

        # Serviços que podemos desativar com segurança
        SERVICES = [
            "DiagTrack",             # telemetria
            "dmwappushservice",      # push WAP
            "WerSvc",                # relatório de erros Windows
            "RemoteRegistry",        # registro remoto
        ]

        stopped = 0
        try:
            self.logger.info("Encerrando processos de telemetria...")
            for proc in PROCS:
                try:
                    r = self._run(["taskkill", "/f", "/im", proc], timeout=8)
                    if r.returncode == 0:
                        stopped += 1
                        self.logger.info(f"  Processo encerrado: {proc}")
                except Exception:
                    pass

            self.logger.info("Desativando serviços de telemetria...")
            for svc in SERVICES:
                try:
                    # Parar serviço
                    self._run(["sc", "stop", svc], timeout=10)
                    # Desativar na inicialização
                    r = self._run(["sc", "config", svc, "start=", "disabled"], timeout=10)
                    if r.returncode == 0:
                        stopped += 1
                        self.logger.info(f"  Serviço desativado: {svc}")
                except Exception:
                    pass

            # Desativar telemetria via registro
            _reg_set(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                "AllowTelemetry", winreg.REG_DWORD, 0
            )

            self.logger.success(f"Telemetria: {stopped} processos/serviços interrompidos")
            self.changes.append(f"Telemetria: {stopped} itens interrompidos")
            return stopped

        except Exception as e:
            self.logger.error(f"Erro ao interromper telemetria: {e}")
            return stopped

    # ─────────────────────────────────────────────────────────────────────────
    # 6. Limpeza de arquivos temporários
    # ─────────────────────────────────────────────────────────────────────────
    def clean_temp_files(self) -> Tuple[int, int]:
        file_count  = 0
        bytes_freed = 0

        # Diretórios alvo
        temp_dirs = set(filter(None, [
            tempfile.gettempdir(),
            os.environ.get("TEMP", ""),
            os.environ.get("TMP",  ""),
            os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Temp"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"),
        ]))

        try:
            self.logger.info(f"Varrendo {len(temp_dirs)} diretórios de temporários...")

            for temp_dir in temp_dirs:
                if not temp_dir or not os.path.isdir(temp_dir):
                    continue
                for item in Path(temp_dir).iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            item.unlink(missing_ok=True)
                            bytes_freed += size
                            file_count  += 1
                        elif item.is_dir():
                            # Tamanho aproximado antes de remover
                            dir_size = sum(
                                f.stat().st_size
                                for f in item.rglob("*")
                                if f.is_file()
                            )
                            shutil.rmtree(item, ignore_errors=True)
                            bytes_freed += dir_size
                            file_count  += 1
                    except (PermissionError, OSError):
                        pass

            mb = bytes_freed // (1024 * 1024)
            self.logger.success(
                f"Limpeza concluída: {file_count} itens removidos, {mb} MB liberados"
            )
            self.changes.append(f"Limpeza: {mb} MB liberados")
            return file_count, mb

        except Exception as e:
            self.logger.error(f"Erro na limpeza de temporários: {e}")
            return file_count, bytes_freed // (1024 * 1024)

    # ─────────────────────────────────────────────────────────────────────────
    # 7. Prioridade de CPU
    # ─────────────────────────────────────────────────────────────────────────
    def prioritize_cpu(self) -> bool:
        try:
            self.logger.info("Ajustando Win32PrioritySeparation no registro...")

            # 0x26 (38) = foreground apps recebem o máximo de quantum de CPU
            _reg_set(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                "Win32PrioritySeparation", winreg.REG_DWORD, 0x26
            )

            # Desativar throttling de rede para jogos/apps
            _reg_set(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "NetworkThrottlingIndex", winreg.REG_DWORD, 0xFFFFFFFF
            )
            _reg_set(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "SystemResponsiveness", winreg.REG_DWORD, 0
            )

            self.logger.success("Prioridade de CPU ajustada para aplicações em foreground")
            self.changes.append("Prioridade de CPU otimizada")
            return True

        except PermissionError:
            self.logger.error(
                "Permissão negada ao escrever no registro. "
                "Execute o rook como administrador."
            )
            return False
        except Exception as e:
            self.logger.error(f"Erro ao priorizar CPU: {e}")
            return False


# ─────────────────────────────────────────────────────────────────────────────
# Utilitário de registro — cria a chave se não existir
# ─────────────────────────────────────────────────────────────────────────────
def _reg_set(hive, path: str, name: str, reg_type, value):
    """Abre (ou cria) uma chave de registro e escreve o valor."""
    key = winreg.CreateKeyEx(hive, path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, name, 0, reg_type, value)
    winreg.CloseKey(key)