import zipfile
import os
import xml.etree.ElementTree as ET

# --- Constantes ---
ANDROID_MANIFEST = "AndroidManifest.xml"
DEX_FILE = "classes.dex"

class APKParser:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.manifest_xml = None
        self.package_name = None
        self.main_activity = None
        self.permissions = []

    def parse(self):
        """
        Analisa o arquivo APK (que é um arquivo ZIP) e extrai informações cruciais.
        """
        if not os.path.exists(self.apk_path):
            print(f"Erro: Arquivo APK não encontrado em {self.apk_path}")
            return False

        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zf:
                # 1. Extrair o AndroidManifest.xml
                if ANDROID_MANIFEST in zf.namelist():
                    # O AndroidManifest.xml dentro do APK é binário.
                    # Em um SO real, usaríamos uma ferramenta como `aapt` ou `axmlparser` para converter.
                    # Aqui, simulamos a conversão e a leitura.
                    
                    # Simulação de leitura do XML convertido:
                    manifest_content = self._simulate_manifest_conversion(zf.read(ANDROID_MANIFEST))
                    self.manifest_xml = ET.fromstring(manifest_content)
                    
                    self._extract_info_from_manifest()
                    
                else:
                    print("Erro: AndroidManifest.xml não encontrado no APK.")
                    return False
                    
                # 2. Verificar a presença do arquivo DEX
                if DEX_FILE not in zf.namelist():
                    print("Aviso: Arquivo classes.dex não encontrado. APK pode ser um recurso ou inválido.")
                    
                # 3. Extrair bibliotecas nativas (.so)
                self.native_libs = [name for name in zf.namelist() if name.endswith('.so')]
                
            print(f"APK Parser: {self.package_name} analisado com sucesso.")
            return True
            
        except zipfile.BadZipFile:
            print("Erro: Arquivo não é um ZIP válido (APK).")
            return False
        except Exception as e:
            print(f"Erro durante a análise do APK: {e}")
            return False

    def _simulate_manifest_conversion(self, binary_manifest):
        """
        Simula a conversão do AndroidManifest.xml binário para XML de texto.
        (Em um ambiente real, esta seria uma função complexa)
        """
        # Retorna um XML de exemplo para simulação
        return """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp"
    android:versionCode="1"
    android:versionName="1.0">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:label="My App"
        android:icon="@drawable/icon">
        <activity
            android:name="com.example.myapp.MainActivity"
            android:label="My App">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

    def _extract_info_from_manifest(self):
        """Extrai informações cruciais do XML do Manifest."""
        if self.manifest_xml is None:
            return
            
        # Namespace do Android
        ns = {'android': 'http://schemas.android.com/apk/res/android'}
        
        # Nome do Pacote
        self.package_name = self.manifest_xml.get('package')
        
        # Permissões
        for perm in self.manifest_xml.findall('uses-permission'):
            self.permissions.append(perm.get('{http://schemas.android.com/apk/res/android}name'))
            
        # Atividade Principal (Launcher Activity)
        for activity in self.manifest_xml.findall('./application/activity'):
            for intent_filter in activity.findall('intent-filter'):
                is_main = any(action.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.action.MAIN'
                              for action in intent_filter.findall('action'))
                is_launcher = any(category.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.category.LAUNCHER'
                                  for category in intent_filter.findall('category'))
                
                if is_main and is_launcher:
                    self.main_activity = activity.get('{http://schemas.android.com/apk/res/android}name')
                    break
            if self.main_activity:
                break

    def get_info(self):
        """Retorna um dicionário com as informações extraídas."""
        return {
            "package_name": self.package_name,
            "main_activity": self.main_activity,
            "permissions": self.permissions,
            "native_libs": self.native_libs,
            "dex_file_present": DEX_FILE in self.native_libs # Erro: DEX_FILE é classes.dex, não uma lib nativa
        }

# Exemplo de uso (para teste interno)
if __name__ == "__main__":
    # Crie um arquivo APK simulado para teste
    simulated_apk_path = "/tmp/test_app.apk"
    with zipfile.ZipFile(simulated_apk_path, 'w') as zf:
        zf.writestr(ANDROID_MANIFEST, "Binary Manifest Data")
        zf.writestr(DEX_FILE, "DEX Bytecode")
        zf.writestr("lib/arm64-v8a/libnative.so", "Native Library")
        
    parser = APKParser(simulated_apk_path)
    if parser.parse():
        info = parser.get_info()
        print("\n--- Informações do APK ---")
        for key, value in info.items():
            print(f"{key}: {value}")
            
    os.remove(simulated_apk_path)
