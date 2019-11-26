# PCS3422 - Organização e Arquitetura de Computadores II

# Boot de Linux (Grupo J)
Este projeto foi realizado pelos seguintes alunos:

Eric Koji Yang Imai Nº USP 9373712
Fábio Fusimoto Pires Nº USP 9853294
Gabriel Roberti Passini Nº USP 9868071
Júlia Fernandes Moraes Nº USP 8988104
Renato de Oliveira Freitas Nº USP 9837708

### Aviso
![](https://findicons.com/files/icons/1676/primo/128/warning_black.png) ![](https://findicons.com/files/icons/1676/primo/128/warning_black.png)  ![](https://findicons.com/files/icons/1676/primo/128/warning_black.png) ![](https://findicons.com/files/icons/1676/primo/128/warning_black.png) 

Os arquivos fonte necessários para a execução desse projeto, bem como o relatório de implementação e os slides da apresentação, estão disponíveis no link abaixo (para acessá-lo, basta fazer o login através de uma conta da USP):

[Repositório no Google Drive](https://drive.google.com/open?id=1KwIvPNgA8LusirV3Iff0n3AIyTtPReAB)

Optou-se por fazer o upload no Drive porque ocorreu um erro ao realizar um push para o Git da disciplina. Isso ocorre porque algumas pastas que contêm os arquivos fonte foram clonadas de outros repositórios do próprio Git e algumas contém arquivos com extensões .git ou outras extensões que o GitHub usa para organizar os diretórios. Logo, a fim de não ter de renomear as pastas (que pode fazer com que os programas não funcionassem direito), optou-se por fazer o upload dos arquivos no Drive.
Se ocorrer algum problema na execução, enviar um email para fabiofusimoto.pires@hotmail.com ou fabio.fusimoto.pires@usp.br

### Objetivos do projeto
- Estudar e compreender o processo de boot do sistema operacional Linux em um sistema embarcado
- Emular a execução do Linux em um processador ARMv8 (sendo o LEGv8, ISA proposto pela disciplina, um subconjunto do ARMv8)
- Listar as adaptações necessárias para executar o Linux no processador LEGv8 (dando suporte aos demais componentes a ele relacionado) desenvolvido por outros grupos da mesma disciplina

### Programas utilizados
- QEMU v1:2.11 (a versão inclusa no Drive está preparada para emular a arquitetura AArch64)
- Buildroot 2019.02.6 (não incluso do Drive, mas não é necessário para executar as simulações)

### Instruções para simulação
Assume-se que o usuário esteja trabalhando com alguma distribuição do Linux baseada em Debian (todos os comando descritos nesse texto foram testados no Ubuntu 18.04 e operam corretamente). Após clonar o repositório do Drive, instalam-se as dependências do QEMU:

`$ sudo apt-get install git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev`

Partindo do diretório raiz (o que contém as pastas images, qemu e texts), pode-se executar uma emulação tendo como saída serial utilizando-se o seguinte comando:

`$ ./qemu/qemu.git/aarch64-softmmu/qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -nographic`

Para interromper a simulação e abrir a janela de comando do QEMU, tecla-se Ctrl+A → C, que disponibiliza uma série de comandos (consultar seção 2.6 da documentação do QEMU, presente no link https://qemu.weilnetz.de/doc/qemu-doc.html#pcsys_005fmonitor, para maiores detalhes). Para encerrar a simulação,  tecla-se Ctrl+A → X.
Se o objetivo for direcionar a comunicação para uma porta serial, executa-se:

`$ ./qemu/qemu.git/aarch64-softmmu/qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -serial /caminho/para/Serial`

As seriais normalmente estão mapeadas nos diretórios /dev/ttyS# ou /dev/ttyUSB# se for uma serial USB. Existe a opção de emular uma serial virtual, isso é feito executando-se:

`./qemu/qemu.git/aarch64-softmmu/qemu-system-aarch64 -cpu cortex-a53 -machine type=virt -kernel ./images/Image -initrd ./images/rootfs.cpio -serial pty`

As mensagens do terminal vão determinar o nome da serial criada (ver seção 6 do relatório para mais detalhes). Para visualizar a troca de mensagens através da serial, recomenda-se o uso do Minicom. Para instalar, executa-se:

`sudo apt-get install minicom`

Configura-se a comunicação executando-se: 

`sudo minicom -s`

Seleciona-se a opção ‘Serial Port Setup’ e altera-se as seguintes configurações: Serial Device: /dev/pts/N (onde N pode variar, mas é observável no terminal mediante a execução do QEMU) e Bps/Par/Bits: 9600 8N1. Uma vez que a configuração for realizada, escolhe-se a opção 'Save Setup as dfl' e seleciona-se 'Exit', que deve iniciar a comunicação imediatamente.

### Divisão de tarefas
- Júlia - Estudo acerca do processo de Boot de Linux em sistemas embarcados, destacando os programas, recursos e arquivos envolvidos. Responsável também pela formatação e revisão do relatório.
- Gabriel - Entendimento acerca do QEMU, suas funcionalidades, parâmetros de execução e recursos emulados.
- Renato - Familiarização com o Buildroot e seu processo de configuração. *Build* dos programas fonte.
- Fábio - Estudo das adaptações necessárias para execução no sistema real, assumindo implementação do LEGv8 numa FPGA. Coordenação e divisão das tarefas e revisão do relatório.
- Eric - Entedimento sobre o processo de *deploy*, isto é, como fazer o Linux rodar na FPGA uma vez que todas as adaptações necessárias estiverem prontas.