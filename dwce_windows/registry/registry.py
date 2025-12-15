import json
import os

# Caminho para o arquivo de registro emulado no Winlinos
REGISTRY_FILE = "/home/ubuntu/.dwce_registry.json"

# Estrutura de registro em memória (simulação)
registry_data = {
    "HKEY_LOCAL_MACHINE": {
        "Software": {
            "Microsoft": {
                "Windows": {
                    "CurrentVersion": {
                        "ProgramFilesDir": "C:\\Program Files",
                        "SystemRoot": "C:\\Windows"
                    }
                }
            }
        }
    },
    "HKEY_CURRENT_USER": {
        "Software": {}
    }
}

def _load_registry():
    """Carrega o registro do disco (se existir)."""
    global registry_data
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r') as f:
                registry_data = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar registro: {e}. Usando registro padrão.")

def _save_registry():
    """Salva o registro no disco."""
    try:
        with open(REGISTRY_FILE, 'w') as f:
            json.dump(registry_data, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar registro: {e}")

def RegOpenKeyExA(hKey, lpSubKey, ulOptions, samDesired):
    """
    Simula a função RegOpenKeyExA.
    Abre a chave de registro especificada.
    """
    print(f"Registry: RegOpenKeyExA chamado para: {hKey} -> {lpSubKey}")
    
    # Mapeamento de HKEY (simulação)
    if hKey == "HKEY_LOCAL_MACHINE":
        root = registry_data["HKEY_LOCAL_MACHINE"]
    elif hKey == "HKEY_CURRENT_USER":
        root = registry_data["HKEY_CURRENT_USER"]
    else:
        # Simulação de erro
        return None 
        
    # Navegar pela subchave
    current_key = root
    try:
        for part in lpSubKey.split('\\'):
            if part in current_key:
                current_key = current_key[part]
            else:
                # Chave não encontrada
                return None
        # Retorna um "handle" (referência à chave)
        return current_key
    except Exception:
        return None

def RegQueryValueExA(hKey, lpValueName):
    """
    Simula a função RegQueryValueExA.
    Recupera o tipo e os dados associados ao nome de valor especificado.
    """
    print(f"Registry: RegQueryValueExA chamado para valor: {lpValueName}")
    
    # hKey é o "handle" retornado por RegOpenKeyExA (a referência Python)
    if isinstance(hKey, dict) and lpValueName in hKey:
        value = hKey[lpValueName]
        # Simulação de retorno (Tipo: REG_SZ, Dados: valor)
        return "REG_SZ", value
    else:
        # Valor não encontrado
        return None, None

def RegSetValueExA(hKey, lpValueName, dwType, lpData):
    """
    Simula a função RegSetValueExA.
    Define os dados e o tipo de um valor em uma chave de registro.
    """
    print(f"Registry: RegSetValueExA chamado para definir {lpValueName} = {lpData}")
    
    if isinstance(hKey, dict):
        hKey[lpValueName] = lpData
        _save_registry()
        return True
    else:
        return False

# Inicializa o registro ao carregar o módulo
_load_registry()

# Exemplo de uso (para teste interno)
if __name__ == "__main__":
    # Abrir a chave
    key_handle = RegOpenKeyExA("HKEY_LOCAL_MACHINE", "Software\\Microsoft\\Windows\\CurrentVersion", 0, 0)
    
    if key_handle:
        # Consultar um valor
        reg_type, value = RegQueryValueExA(key_handle, "ProgramFilesDir")
        print(f"ProgramFilesDir: {value}") # Deve retornar C:\Program Files
        
        # Definir um novo valor
        new_key_handle = RegOpenKeyExA("HKEY_CURRENT_USER", "Software", 0, 0)
        RegSetValueExA(new_key_handle, "MeuApp", "REG_SZ", "Instalado")
        
        # Consultar o novo valor
        reg_type, new_value = RegQueryValueExA(new_key_handle, "MeuApp")
        print(f"MeuApp: {new_value}") # Deve retornar Instalado
    else:
        print("Erro ao abrir chave.")
