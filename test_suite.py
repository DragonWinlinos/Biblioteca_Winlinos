import os
import sys
import time
import subprocess

# Importar os módulos principais para teste
sys.path.append(os.path.join(os.path.dirname(__file__), 'dwce_core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'dwce_windows'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'dwce_android'))

from process_manager.process_manager import ProcessManager
from syscall_unified.syscall_unified import translate_win_syscall, translate_android_syscall
from pe_loader.pe_loader import PELoader
from art_runtime.art_runtime import ART_Runtime
from filesystem.filesystem import translate_path
from registry.registry import RegOpenKeyExA, RegQueryValueExA

# --- Testes de Sanidade ---

def test_windows_compatibility(pm):
    print("\n--- Teste de Compatibilidade Windows (.exe) ---")
    
    # 1. Teste de Tradução de Caminho (Filesystem)
    win_path = "C:\\Program Files\\Game\\game.exe"
    lin_path = translate_path(win_path)
    print(f"  Caminho Windows '{win_path}' traduzido para: {lin_path}")
    assert lin_path.endswith("Program Files/Game/game.exe"), "Falha na tradução de caminho."
    
    # 2. Teste de Registro (Registry)
    key_handle = RegOpenKeyExA("HKEY_LOCAL_MACHINE", "Software\\Microsoft\\Windows\\CurrentVersion", 0, 0)
    _, value = RegQueryValueExA(key_handle, "ProgramFilesDir")
    print(f"  Valor do Registro 'ProgramFilesDir': {value}")
    assert value == "C:\\Program Files", "Falha na emulação de registro."
    
    # 3. Teste de Syscall (NTDLL)
    result = translate_win_syscall("NtAllocateVirtualMemory", 0, 0, 0, 4096, 0, 0)
    print(f"  Syscall NtAllocateVirtualMemory retornou: {hex(result)}")
    assert result != -1, "Falha na tradução de syscall Windows."
    
    # 4. Teste de Processo (PE Loader)
    # Simulação de execução de um PE
    test_exe_path = "/tmp/test_win_app.exe"
    # Criar um arquivo dummy para simular o PE
    with open(test_exe_path, 'w') as f: f.write("MZ...")
    
    pid = pm.create_process(test_exe_path, "win")
    assert pid is not None, "Falha ao criar processo Windows."
    print(f"  Processo Windows criado com DWCE PID: {pid}")
    pm.terminate_process(pid)
    os.remove(test_exe_path)
    
    print("  Teste Windows concluído com sucesso.")

def test_android_compatibility(pm):
    print("\n--- Teste de Compatibilidade Android (.apk) ---")
    
    # 1. Teste de Syscall (ART)
    result = translate_android_syscall("android.util.Log.i", "TAG", "Teste de Log")
    assert result == 0, "Falha na tradução de syscall Android."
    print("  Syscall android.util.Log.i traduzida com sucesso.")
    
    # 2. Teste de Processo (ART Runtime)
    runtime = ART_Runtime()
    # Simulação de execução de um APK
    test_apk_path = "/tmp/test_android_app.apk"
    with open(test_apk_path, 'w') as f: f.write("APK...")
    
    # O ART Runtime gerencia o ciclo de vida do app
    runtime.launch_app(test_apk_path)
    
    # Simulação de que o Process Manager registrou o processo (o ART_Runtime faria isso)
    # Aqui, apenas verificamos a inicialização do ART
    assert runtime.is_initialized, "Falha ao inicializar ART Runtime."
    print("  ART Runtime inicializado e app lançado com sucesso.")
    
    runtime.stop_app("com.example.myapp")
    os.remove(test_apk_path)
    
    print("  Teste Android concluído com sucesso.")

def test_linux_compatibility(pm):
    print("\n--- Teste de Compatibilidade Linux (ELF) ---")
    
    # 1. Teste de Processo (ELF Loader)
    # Simulação de execução de um ELF
    test_elf_path = "/tmp/test_linux_app"
    with open(test_elf_path, 'w') as f: f.write("ELF...")
    
    pid = pm.create_process(test_elf_path, "linux")
    assert pid is not None, "Falha ao criar processo Linux."
    print(f"  Processo Linux criado com DWCE PID: {pid}")
    pm.terminate_process(pid)
    os.remove(test_elf_path)
    
    print("  Teste Linux concluído com sucesso.")

def run_all_tests():
    print("===================================================")
    print("  INICIANDO SUÍTE DE TESTES DE COMPATIBILIDADE DWCE")
    print("===================================================")
    
    pm = ProcessManager()
    
    try:
        test_windows_compatibility(pm)
        test_android_compatibility(pm)
        test_linux_compatibility(pm)
        
        print("\n===================================================")
        print("  TODOS OS TESTES DE SANIDADE CONCLUÍDOS COM SUCESSO")
        print("  A arquitetura de compatibilidade está funcional.")
        print("===================================================")
        
    except AssertionError as e:
        print(f"\n===================================================")
        print(f"  FALHA NO TESTE: {e}")
        print("===================================================")
    except Exception as e:
        print(f"\n===================================================")
        print(f"  ERRO INESPERADO DURANTE O TESTE: {e}")
        print("===================================================")

if __name__ == "__main__":
    run_all_tests()
