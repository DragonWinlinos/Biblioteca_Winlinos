import sys
import os
import importlib.util

# Adiciona o diretório do DWCE Core ao PATH para importação
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dragon-winlinos-compatibility-engine'))

try:
    import dwce_core
except ImportError:
    print("Erro: dwce_core não encontrado. O sistema de compatibilidade não pode ser inicializado.")
    # Fallback para 32bit se o core não for encontrado
    class FallbackTools:
        def run_optimized_task(self, task_name):
            return f"Task '{task_name}' executed with Fallback 32-bit system calls."
        def get_system_hash(self):
            return "HASH_FALLBACK_32BIT"
    
    # Simula a importação das ferramentas
    run_optimized_task = FallbackTools().run_optimized_task
    get_system_hash = FallbackTools().get_system_hash
    
else:
    # 1. Determina o caminho da biblioteca otimizada
    base_path = os.path.dirname(__file__)
    optimized_path = dwce_core.select_library_path(base_path)
    
    # 2. Carrega o módulo system_tools a partir do caminho otimizado
    module_path = os.path.join(optimized_path, "system_tools.py")
    module_name = "system_tools_optimized"
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Não foi possível encontrar o módulo em: {module_path}")
        
    system_tools = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = system_tools
    spec.loader.exec_module(system_tools)
    
    # 3. Exporta as funções do motor carregado
    run_optimized_task = system_tools.run_optimized_task
    get_system_hash = system_tools.get_system_hash

# Exemplo de uso:
# print(run_optimized_task("Backup"))
# print(get_system_hash())
