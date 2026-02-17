# modules/services_optimizer.py
from typing import Dict, List
from .base_optimizer import BaseOptimizer

class ServicesOptimizer(BaseOptimizer):
    """Gerencia serviços do Windows"""
    
    def __init__(self):
        super().__init__()
        self.services_to_disable = {
            # Serviços de desempenho
            "SysMain": "Superfetch/ReadyBoost - Pode causar alto uso de disco",
            "WSearch": "Windows Search - Indexação de arquivos",
            
            # Serviços Xbox
            "XboxNetApiSvc": "Xbox Live Networking",
            "XblAuthManager": "Xbox Live Auth Manager",
            "XblGameSave": "Xbox Live Game Save",
            "XboxGipSvc": "Xbox Accessory Management",
            
            # Serviços de fax e impressão
            "Fax": "Fax Service",
            "PrintSpooler": "Spooler de impressão (se não usar impressora)",
            
            # Serviços de rede e registro
            "RemoteRegistry": "Remote Registry - Permite acesso remoto ao registro",
            
            # Serviços de telemetria
            "DiagTrack": "Connected User Experiences and Telemetry",
            "dmwappushservice": "Device Management WAP Push",
            
            # Serviços de sincronização
            "OneSyncSvc": "Sync Host",
            "UserDataSvc": "User Data Access",
            
            # Outros serviços desnecessários
            "lfsvc": "Geolocation Service",
            "MapsBroker": "Downloaded Maps Manager",
            "PcaSvc": "Program Compatibility Assistant",
            "WMPNetworkSvc": "Windows Media Player Network Sharing",
            "RetailDemo": "Retail Demo Service",
            "WpnService": "Windows Push Notifications",
            "StorSvc": "Storage Service",
        }
        
        self.services_state = {}
        
    def get_service_status(self, service_name: str) -> Dict:
        """Obtém status atual do serviço"""
        try:
            success, output = self.run_cmd_command(f'sc query {service_name}')
            if success:
                lines = output.split('\n')
                status = {}
                for line in lines:
                    if 'STATE' in line:
                        status['state'] = 'running' if 'RUNNING' in line else 'stopped'
                    elif 'START_TYPE' in line:
                        status['start_type'] = 'auto' if 'AUTO' in line else 'manual' if 'DEMAND' in line else 'disabled'
                return status
        except:
            pass
        return {}
    
    def disable_service(self, service_name: str, reason: str = "") -> bool:
        """Desabilita um serviço específico"""
        try:
            # Salvar estado atual antes de modificar
            current_state = self.get_service_status(service_name)
            self.services_state[service_name] = current_state
            
            # Desabilitar serviço
            success = self.enable_disable_service(service_name, enable=False)
            
            if success:
                self.changes_made.append(f"Service disabled: {service_name} - {reason}")
                self.logger.log_action(f"Serviço {service_name} desabilitado", "SUCCESS")
            else:
                self.errors.append(f"Failed to disable {service_name}")
                
            return success
        except Exception as e:
            self.errors.append(f"Erro desabilitando {service_name}: {str(e)}")
            return False
    
    def apply(self) -> bool:
        """Aplica otimizações de serviços"""
        try:
            self.logger.log_action("Iniciando otimização de serviços", "INFO")
            
            disabled_count = 0
            for service, reason in self.services_to_disable.items():
                if self.disable_service(service, reason):
                    disabled_count += 1
            
            self.logger.log_action(f"{disabled_count} serviços otimizados", "SUCCESS")
            return True
        except Exception as e:
            self.logger.log_action(f"Erro otimização serviços: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Reverte serviços ao estado anterior"""
        try:
            for service, state in self.services_state.items():
                if state and state.get('start_type') == 'auto':
                    self.enable_disable_service(service, enable=True)
            return True
        except:
            return False