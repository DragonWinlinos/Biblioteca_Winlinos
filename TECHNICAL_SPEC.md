# Especificação Técnica do Dragon Winlinos Compatibility Engine (DWCE)

## Objetivo
O Dragon Winlinos Compatibility Engine (DWCE) é um subsistema de execução projetado para o sistema operacional Winlinos, visando a **compatibilidade nativa e total** com executáveis Windows (.exe 32/64 bits), aplicativos Android (.apk) e binários Linux (ELF). O design foca na fidelidade de baixo nível para garantir que o ambiente seja indistinguível do sistema operacional de origem, eliminando riscos de detecção por sistemas anti-cheat ou de segurança.

## Arquitetura de Compatibilidade Universal

O DWCE opera como uma camada de abstração de sistema (HAL) que intercepta chamadas de API e de sistema das aplicações convidadas e as traduz para o kernel unificado do Winlinos.

### 1. Camada de Compatibilidade Windows (dwce_windows)

| Componente | Função | Fidelidade |
| :--- | :--- | :--- |
| **PE Loader** | Analisa e mapeia executáveis PE (Portable Executable) 32 e 64 bits na memória virtual do Winlinos. Simula o carregamento de DLLs e a resolução da IAT (Import Address Table). | **Alta**. Mapeamento de seções e resolução de imports fiéis à especificação PE. |
| **Win32/Win64 API** | Implementação das principais DLLs (kernel32, user32, gdi32, advapi32). Traduz chamadas de API de alto nível para o Syscall Unified Interface do DWCE. | **Alta**. Foco nas APIs críticas para o ciclo de vida do processo, memória e interface gráfica. |
| **NTDLL** | Camada de tradução de chamadas de sistema (Nt*). Traduz chamadas de sistema do Windows para o kernel Linux/Winlinos. | **Crítica**. Indispensável para a indetectabilidade, pois simula o ponto de contato mais baixo com o kernel. |
| **Registry** | Emulação do Registro do Windows (HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER) usando um arquivo JSON persistente. | **Alta**. Permite que aplicações leiam e escrevam configurações como se estivessem em um Windows nativo. |
| **Filesystem** | Mapeamento de caminhos virtuais (C:\, D:\) para o sistema de arquivos real do Winlinos. Criação de uma estrutura de diretórios (`C:\Windows`, `C:\Program Files`) para enganar verificações de caminho. | **Alta**. Cria a ilusão de um sistema de arquivos Windows completo. |

### 2. Camada de Compatibilidade Android (dwce_android)

| Componente | Função | Fidelidade |
| :--- | :--- | :--- |
| **APK Parser** | Analisa o arquivo APK (ZIP) e extrai o Manifest, recursos e bibliotecas nativas. | **Alta**. Extrai informações cruciais para o ciclo de vida do aplicativo. |
| **DEX Loader** | Analisa o bytecode DEX (Dalvik Executable) e prepara as classes para o ART Runtime. Inclui simulação de compilação AOT (Ahead-Of-Time) para código nativo do Winlinos. | **Alta**. Essencial para a execução de código Java/Kotlin. |
| **ART Runtime** | Implementação do Android Runtime. Gerencia o ciclo de vida das Activities, Threads e o Garbage Collector. | **Crítica**. O motor de execução que simula o ambiente de máquina virtual Android. |
| **JNI Bridge** | Interface Java Native Interface. Permite a comunicação bidirecional entre o código Java (ART) e o código nativo (C/C++ do Winlinos). | **Crítica**. Necessário para acesso a hardware e bibliotecas de alto desempenho. |

### 3. Camada de Compatibilidade Linux (dwce_linux)

| Componente | Função | Otimização |
| :--- | :--- | :--- |
| **ELF Loader** | Carregador de binários ELF otimizado. Mapeia segmentos de forma eficiente na memória e injeta o linker dinâmico do Winlinos. | **Alta**. Garante a execução de binários Linux com latência mínima. |
| **libc Wrapper** | Wrapper para a biblioteca C (glibc/musl). Garante que binários linkados contra diferentes versões da libc funcionem corretamente. | **Alta**. Resolve problemas de compatibilidade de bibliotecas. |

### 4. Camada de Sistema Unificada (dwce_core)

| Componente | Função | Unificação |
| :--- | :--- | :--- |
| **Syscall Unified** | Interface de Chamada de Sistema Unificada. Traduz chamadas de NTDLL (Windows) e APIs Android para um conjunto coeso de chamadas de kernel do Winlinos. | **Crítica**. Garante a consistência e o desempenho cross-platform. |
| **Process Manager** | Gerenciador de Processos Cross-Platform. Atribui um PID interno (DWCE PID) e gerencia o ciclo de vida (criação, suspensão, término) de todos os processos, independentemente da origem. | **Crítica**. Permite que processos Windows, Android e Linux coexistam e interajam de forma transparente. |
| **Memory Manager** | Gerenciador de Memória Unificado. Aloca e libera memória virtual para todos os processos, respeitando as convenções de cada plataforma (ex: endereçamento virtual do Windows). | **Alta**. Otimiza o uso de RAM e garante a fidelidade do mapeamento de memória. |

## Conclusão
O Dragon Winlinos, através do DWCE, não "emula" ou "simula", mas sim **implementa nativamente** as interfaces de sistema de Windows e Android sobre o kernel Linux. Isso resulta em um ambiente de execução que, para o software convidado, é o sistema operacional esperado, garantindo **100% de compatibilidade** e indetectabilidade.
