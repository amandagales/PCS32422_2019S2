# PCS3422 - Organização e Arquitetura de Computadores II

# Boot de Linux (Grupo J)
Este projeto foi realizado pelos seguintes alunos:

Eric Koji Yang Imai Nº USP 9373712

Fábio Fusimoto Pires Nº USP 9853294

Gabriel Roberti Passini Nº USP 9868071

Julia Fernandes Moraes Nº USP 8988104

Renato de Oliveira Freitas Nº USP 9837708


### Objetivos do projeto
- Estudar e compreender o processo de boot do sistema operacional Linux em um sistema embarcado
- Emular a execução do Linux em um processador ARMv8 (sendo o LEGv8, ISA proposto pela disciplina, um subconjunto do ARMv8)
- Listar as adaptações necessárias para executar o Linux no processador LEGv8 (dando suporte aos demais componentes a ele relacionado) desenvolvido por outros grupos da mesma disciplina

### Programas utilizados
- QEMU v2.11.1 
- Buildroot 2019.02.6 (não é necessário para executar as simulações)

### Instruções para simulação
Assume-se que o usuário esteja trabalhando com alguma distribuição do Linux baseada em Debian (todos os comando descritos nesse texto foram testados no Ubuntu 18.04 e operam corretamente). Todos os detalhes de execução estão descritos no relatório. Para instalar o QEMU:

`$ sudo apt install libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev`

`$ sudo apt install qemu-utils qemu-efi-aarch64 qemu-system-arm` 

Partindo do diretório raiz (o que contém as pastas images e texts), pode-se executar uma emulação tendo como saída serial utilizando-se o seguinte comando:

`$ qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -nographic`

Para interromper a simulação e abrir a janela de comando do QEMU, tecla-se Ctrl+A → C, que disponibiliza uma série de comandos (consultar seção 2.6 da documentação do QEMU, presente no link https://qemu.weilnetz.de/doc/qemu-doc.html#pcsys_005fmonitor, para maiores detalhes). Para encerrar a simulação,  tecla-se Ctrl+A → X.
Se o objetivo for direcionar a saída para uma porta serial, executa-se:

`$ qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -serial /caminho/para/Serial`

As seriais normalmente estão mapeadas nos diretórios /dev/ttyS# ou /dev/ttyUSB# se for uma serial USB. Existe a opção de emular uma serial virtual, isso é feito executando-se:

`$ qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -serial pty`

As mensagens do terminal vão determinar o nome da serial criada (ver seção 6 do relatório para mais detalhes). Para visualizar a troca de mensagens através da serial, recomenda-se o uso do Minicom. Para instalar, executa-se:

`sudo apt install minicom`

Configura-se a comunicação executando-se: 

`sudo minicom -s`

Seleciona-se a opção ‘Serial Port Setup’ e altera-se as seguintes configurações: Serial Device: /dev/pts/N (onde N pode variar, mas é observável no terminal mediante a execução do QEMU) e Bps/Par/Bits: 9600 8N1. Uma vez que a configuração for realizada, escolhe-se a opção 'Save Setup as dfl' e seleciona-se 'Exit', que deve iniciar a comunicação imediatamente.

### Divisão de tarefas
- Julia - Estudo acerca do processo de Boot de Linux em sistemas embarcados, destacando os programas, recursos e arquivos envolvidos. Responsável também pela formatação e revisão do relatório.
- Gabriel - Entendimento acerca do QEMU, suas funcionalidades, parâmetros de execução e recursos emulados.
- Renato - Familiarização com o Buildroot e seu processo de configuração. *Build* dos programas fonte.
- Fábio - Estudo das adaptações necessárias para execução no sistema real, assumindo implementação do LEGv8 numa FPGA. Coordenação e divisão das tarefas e revisão do relatório.
- Eric - Entedimento sobre o processo de *deploy*, isto é, como fazer o Linux rodar na FPGA uma vez que todas as adaptações necessárias estiverem prontas.