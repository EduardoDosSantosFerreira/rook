# modules/network_optimizer.py
import subprocess
from .base_optimizer import BaseOptimizer

class NetworkOptimizer(BaseOptimizer):
    """Otimiza configurações de rede"""
    
    def reset_tcp_ip(self) -> bool:
        """Reseta TCP/IP stack"""
        try:
            commands = [
                'netsh int ip reset',
                'netsh winsock reset',
                'netsh int tcp set global autotuninglevel=normal',
                'netsh int tcp set global rss=enabled',
                'netsh int tcp set global chimney=enabled',
                'netsh int tcp set global netdma=enabled'
            ]
            
            for cmd in commands:
                self.run_cmd_command(cmd)
            
            self.changes_made.append("TCP/IP stack reset")
            return True
        except Exception as e:
            self.errors.append(f"Erro reset TCP/IP: {str(e)}")
            return False
    
    def reset_winsock(self) -> bool:
        """Reseta Winsock catalog"""
        try:
            self.run_cmd_command('netsh winsock reset')
            self.changes_made.append("Winsock reset")
            return True
        except Exception as e:
            self.errors.append(f"Erro reset Winsock: {str(e)}")
            return False
    
    def flush_dns(self) -> bool:
        """Limpa cache DNS"""
        try:
            self.run_cmd_command('ipconfig /flushdns')
            self.changes_made.append("DNS cache flushed")
            return True
        except Exception as e:
            self.errors.append(f"Erro flush DNS: {str(e)}")
            return False
    
    def apply(self) -> bool:
        """Aplica otimizações de rede"""
        try:
            self.logger.log_action("Iniciando otimizações de rede", "INFO")
            
            success_count = 0
            
            if self.reset_tcp_ip():
                success_count += 1
                self.logger.log_action("✅ TCP/IP resetado", "SUCCESS")
            
            if self.reset_winsock():
                success_count += 1
                self.logger.log_action("✅ Winsock resetado", "SUCCESS")
            
            if self.flush_dns():
                success_count += 1
                self.logger.log_action("✅ DNS cache limpo", "SUCCESS")
            
            return success_count > 0
        except Exception as e:
            self.logger.log_action(f"Erro otimizações rede: {str(e)}", "ERROR")
            return False
    
    def revert(self) -> bool:
        """Não há reversão simples para rede"""
        return True