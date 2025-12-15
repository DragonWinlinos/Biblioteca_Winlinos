import os
import subprocess
import time
import uuid
import sys

# --- Process Manager (Cross-Platform) ---
# Gerencia o ciclo de vida de todos os processos (Windows, Android, Linux)
# e garante que eles se comportem de acordo com as regras do Winlinos.

class ProcessManager:
    def __init__(self):
        self.active_processes = {} # {dwce_pid: {type: 'win'/'android'/'linux', os_pid: 1234, ...}}
        self.system_arch = "64bit" # Simulação de arquitetura do Winlinos

        self.next_dwce_pid = 1000

    def _generate_dwce_pid(self):
        """Gera um PID interno do Winlinos (DWCE PID)."""
        pid = self.next_dwce_pid
        self.next_dwce_pid += 1
        return pid

    def create_process(self, executable_path, process_type, args=None):
        """
        Cria um novo processo, usando o loader apropriado.
        process_type: 'win', 'android', 'linux'
        """
        dwce_pid = self._generate_dwce_pid()
        print(f"Process Manager: Criando processo {process_type} com DWCE PID: {dwce_pid}")
        
        # 1. Selecionar o Loader/Runtime
        if process_type == 'win':
            # Chama o PE Loader e o ambiente Win32/64
            # Comando de execução simulado:
            command = [sys.executable, "-m", "dwce_windows.pe_loader.pe_loader", executable_path]
        elif process_type == 'android':
            # Chama o ART Runtime
            # Comando de execução simulado:
            command = [sys.executable, "-m", "dwce_android.art_runtime.art_runtime", executable_path]
        elif process_type == 'linux':
            # Chama o ELF Loader
            # Comando de execução simulado:
            command = [sys.executable, "-m", "dwce_linux.elf_loader.elf_loader", executable_path]
        else:
            print(f"Erro: Tipo de processo desconhecido: {process_type}")
            return None

        # 2. Executar o processo (em um SO real, seria um fork/exec)
        try:
            # Usamos subprocess.Popen para simular a execução em segundo plano
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os_pid = process.pid
            
            self.active_processes[dwce_pid] = {
                "type": process_type,
                "os_pid": os_pid,
                "path": executable_path,
                "start_time": time.time(),
                "process_handle": process # Referência ao objeto Popen
            }
            
            print(f"  Processo {dwce_pid} iniciado. OS PID: {os_pid}")
            return dwce_pid
            
        except Exception as e:
            print(f"Erro ao iniciar processo: {e}")
            return None

    def get_system_arch(self):
        """Retorna a arquitetura do sistema Winlinos (para WoW64)."""
        return self.system_arch

    def terminate_process(self, dwce_pid, exit_code=0):
        """
        Termina um processo ativo.
        """
        if dwce_pid not in self.active_processes:
            print(f"Erro: Processo com DWCE PID {dwce_pid} não encontrado.")
            return False
            
        process_info = self.active_processes[dwce_pid]
        process = process_info["process_handle"]
        
        print(f"Process Manager: Terminando processo {dwce_pid} ({process_info['type']})")
        
        try:
            # Envia o sinal de terminação
            process.terminate()
            process.wait(timeout=5) # Espera 5 segundos para o processo terminar
            
            if process.poll() is None:
                # Se ainda não terminou, mata o processo
                process.kill()
                
            del self.active_processes[dwce_pid]
            print(f"  Processo {dwce_pid} terminado com sucesso.")
            return True
            
        except Exception as e:
            print(f"Erro ao terminar processo {dwce_pid}: {e}")
            return False

    def get_process_list(self):
        """Retorna a lista de processos ativos."""
        return list(self.active_processes.values())

# Exemplo de uso (para teste interno)
if __name__ == "__main__":
    pm = ProcessManager()
    
    # Simulação de criação de processos
    win_pid = pm.create_process("/tmp/test.exe", "win")
    android_pid = pm.create_process("/tmp/test.apk", "android")
    
    print("\nLista de Processos Ativos:")
    for p in pm.get_process_list():
        print(f"  DWCE PID: {p['os_pid']} | Tipo: {p['type']} | Caminho: {p['path']}")
        
    time.sleep(1) # Deixa os processos simulados rodarem um pouco
    
    # Simulação de terminação
    if win_pid:
        pm.terminate_process(win_pid)
    if android_pid:
        pm.terminate_process(android_pid)
        
    print("\nLista de Processos Ativos após terminação:")
    print(pm.get_process_list())
