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
    class FallbackEngine:
        def initialize_graphics_engine(self):
            return "DWCE Graphics Engine (Fallback 32-bit)"
        def draw_window(self, title):
            return f"Window '{title}' drawn with Fallback 32-bit rendering."
    
    # Simula a importação do motor de renderização
    initialize_graphics_engine = FallbackEngine().initialize_graphics_engine
    draw_window = FallbackEngine().draw_window
    
else:
    # 1. Determina o caminho da biblioteca otimizada
    base_path = os.path.dirname(__file__)
    optimized_path = dwce_core.select_library_path(base_path)
    
    # 2. Carrega o módulo render_engine a partir do caminho otimizado
    module_path = os.path.join(optimized_path, "render_engine.py")
    module_name = "render_engine_optimized"
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Não foi possível encontrar o módulo em: {module_path}")
        
    render_engine = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = render_engine
    spec.loader.exec_module(render_engine)
    
    # 3. Exporta as funções do motor carregado
    initialize_graphics_engine = render_engine.initialize_graphics_engine
    draw_window = render_engine.draw_window

# Exemplo de uso:
# print(initialize_graphics_engine())
# print(draw_window("Configurações do Sistema"))
