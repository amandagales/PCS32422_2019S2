# Grupo F - Previsão de Desvio

## Organização de arquivos
- Documentos
	- Relatório (em PDF e DOCX)
	- Apresentação do trabalho (em PDF e PPTX)
- ModelSim_BranchTable
	- Projeto com as configurações do ModelSim para a simulação do tabela de previsão de desvios (`BranchTable.mpf`)
	- Instruções de execução da simulação tabela de previsão de desvios (`Wave/wave.do`)
- ModelSim_Pipeline
	- Projeto com as configurações do ModelSim para a simulação do pipeline (`previsao_desvio.mpf`)
	- Instruções de execução da simulação do pipeline (`Wave/wave.do`)
- Quartus
	- Arquivos referentes ao projeto no Quartus
	- Projeto arquivado (`previsao_desvio.qar`)
- src
	- Arquivos fonte do pipeline com previsão de desvio

## Infraestrutura necessária para simular/rodar
- Quartus Prime 18.1 com suporte à família Cyclone IV E.
- ModelSim - Intel FPGA Starter Edition 10.5b (Quartus Prime 18.1)

## Instruções para simular/rodar
### Tabela:
1. Os arquivos para a *testbench* de simulação da tabela estão na pasta `ModelSim_BranchTable`; 
2. Utilizando o **ModelSim**, é possível executar o projeto de testes abrindo o arquivo `ModelSim_BranchTable/table_test.mpf` e então compilando os arquivos (vhd) do projeto.
	- Certifique-se que o compilador está usando a sintaxe 1076-2008. Isso é verificado **selecionando os arquivos > pressionando o botão direito > Compile > Compile Properties > VHDL > Language Syntax > Use 1076-2008**;
3. Selecionar **Simulate** > **Start Simulation** > **work** > **branch_table_tb**;
4. No terminal do **ModelSim**, executar o comando `do wave/wave.do` (Certifique-se que você se encontra no diretório que contém a pasta wave no terminal do **ModelSim**).
5. No terminal do **ModelSim**, executar o comando `run 200ns`.

### Pipeline:
1. Os arquivos para a simulação do *pipeline* estão na pasta `ModelSim_Pipeline` e os arquivos (vhd) do projeto integrado com o pipeline se encontram na pasta `src`; 
2. Utilizando o **ModelSim**, abrir o arquivo `ModelSim_Pipeline/previsao_desvio.mpf` e então compilar os arquivos (vhd) do projeto.
3. Selecionar **Simulate** > **Start Simulation** > **work** > **processor**;
4. No terminal do **ModelSim**, executar o comando `do Wave/wave.do` (Certifique-se que você se encontra no diretório que contém a pasta wave no terminal do **ModelSim**).
5. No terminal do **ModelSim**, executar o comando `run 900ns` (Após o pipeline terminar de executar as instruções na memória, ele tentará acessar uma posição inválida, causando fatal error, por conta da maneira como o pipeline foi feito).

Uma explicação mais aprofundada dos testes, com a explicação de o que cada sinal significa, está presente no relatório do projeto.

## Descrição
O objetivo do projeto do Grupo F foi desenvolver um módulo de previsão de desvio que pudesse ser aplicado a um processador do tipo *LEGv8*. O previsor de desvio dinâmico foi modelado com base no conceito de contador saturado, no caso, de 2 *bits* (4 estados). O módulo foi aplicado ao *pipeline* do Grupo E. Uma explicação mais aprofundada da implementação está presente no relatório do projeto.

## Resumo da participação dos integrantes
- **Bruno Brandão Inácio (9838122)**: Integração e testes com o pipeline do grupo E (Integração/ModelSim);
- **Pedro de Moraes Ligabue (9837434)**: Coordenador do grupo. Adição da tabela de previsão ao pipeline do grupo E (VHDL/Integração);
- **Pedro Henrique L. F. de Mendonça (8039011)**: Descrição da tabela de previsão de desvio e sua Testbench (VHDL/ModelSim);
- **Vitor Tiveron de Almeida Santos (9868085)**: Testes do pipeline do grupo E (ModelSim);
- **Rodrigo Perrucci Macharelli (9348877)**: Testes da tabela de previsão de desvio (ModelSim).