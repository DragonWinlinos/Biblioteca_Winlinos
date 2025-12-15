# Mapeamento de Expansão do Dragon Winlinos Compatibility Engine (DWCE)

Este documento detalha as novas funcionalidades e otimizações a serem implementadas no DWCE, com base na pesquisa aprofundada, visando a **fidelidade estrutural nativa** e a **indistinguibilidade** para o software convidado.

## 1. Otimizações de Compatibilidade Windows (Fidelidade NTDLL)

| Funcionalidade | Módulo Alvo | Descrição | Justificativa (Anti-Cheat) |
| :--- | :--- | :--- | :--- |
| **WoW64 Nativo** | `dwce_windows/win32_api` | Implementação de uma camada de tradução de chamadas 32-bit para 64-bit que replica o comportamento do WoW64 do Windows. | Garante que executáveis 32-bit em um ambiente 64-bit se comportem exatamente como no Windows, evitando anomalias na pilha de chamadas. |
| **Simulação de Estruturas de Kernel** | `dwce_windows/ntdll` | Implementar a simulação das estruturas de dados internas do kernel Windows (ex: VAD - Virtual Address Descriptors, EPROCESS/KPROCESS) no espaço de usuário, acessíveis via NTDLL. | Sistemas anti-cheat de modo usuário frequentemente verificam essas estruturas para detectar VMs ou emuladores. A fidelidade estrutural nativa é a chave. |
| **Syscall Direct Path** | `dwce_windows/ntdll` | Garantir que a tradução de NT Syscalls para o kernel Winlinos utilize o caminho mais direto e otimizado, minimizando o overhead e a chance de *hooking* por terceiros. | Acelera a execução e torna a interceptação mais difícil, replicando a eficiência de uma chamada de sistema nativa. |

## 2. Otimizações de Compatibilidade Android (Fidelidade ART)

| Funcionalidade | Módulo Alvo | Descrição | Justificativa (Desempenho) |
| :--- | :--- | :--- | :--- |
| **Profile-Guided Optimization (PGO) para AOT** | `dwce_android/art_runtime` | Implementar um sistema de coleta de perfil de uso para otimizar a compilação Ahead-Of-Time (AOT) do bytecode DEX. | Melhora a velocidade de inicialização e o desempenho em tempo de execução, replicando as otimizações do ART moderno. |
| **Integração de Memória ART** | `dwce_core/memory_manager` | Otimizar o gerenciador de memória para suportar as estratégias de economia de memória do ART (ex: compactação de heap, gerenciamento de Large Objects). | Essencial para a estabilidade e desempenho de aplicativos Android que dependem de um gerenciamento de memória agressivo. |
| **JNI Bridge de Baixa Latência** | `dwce_android/jni_bridge` | Refatorar o JNI Bridge para minimizar a sobrecarga de transição entre o código Java e o código nativo Winlinos, focando na passagem eficiente de *primitives* e *buffers*. | Reduz o gargalo de desempenho em jogos e aplicações que usam muito código nativo. |

## 3. Otimizações de Compatibilidade Linux (Fidelidade ELF)

| Funcionalidade | Módulo Alvo | Descrição | Justificativa (Desempenho) |
| :--- | :--- | :--- | :--- |
| **ELF Loader Otimizado (Hash)** | `dwce_linux/elf_loader` | Implementar a pré-computação de valores de hash ELF para acelerar a resolução de símbolos e o carregamento de bibliotecas dinâmicas. | Reduz o tempo de inicialização de binários Linux, replicando a eficiência de um linker dinâmico moderno. |
| **vDSO/Userspace Syscall Bypass** | `dwce_core/syscall_unified` | Implementar um mecanismo para lidar com chamadas de sistema comuns (ex: `gettimeofday`, `getcpu`) diretamente no espaço de usuário, sem transição para o kernel. | Minimiza o overhead de syscalls, melhorando o desempenho geral do sistema. |
| **Suporte Avançado a Libc** | `dwce_linux/libc_wrapper` | Expandir o wrapper para lidar com as nuances de ABI entre glibc e musl, garantindo a compatibilidade com a vasta maioria de binários Linux. | Aumenta a compatibilidade com binários estaticamente e dinamicamente linkados. |

## Próxima Fase: Implementação
A próxima fase será a implementação dessas otimizações nos módulos correspondentes do DWCE.
