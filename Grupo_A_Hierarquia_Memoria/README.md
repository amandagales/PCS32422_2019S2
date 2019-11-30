# Hierarquia de Memória com Cache Multinível

## Descrição

Este projeto ilustra o funcionamento de um sistema de hierarquia de memória multinível para um processador ARM. É um trabalho decorrente de um estudo comparativo entre as técnicas de otimização para caches e dessa forma, implementa duas hierarquias a fim de confrontá-las. A primeira, denominada de Hierarquia básica, é uma hierarquia simples, com apenas um nível e sem quaisquer otimizações. A segunda, denominada de Hierarquia Otimizada, evolui a hierarquia primeira implementando algumas otimizações. São elas:

- Associatividade 2-way

- Cache multinível (2 níveis) + memória principal

- Buffer Write-Back

- Política de Exclusion

O estudo detalhado destas técnicas encontra-se no relatório do trabalho, presente na pasta docs.

Este projeto foi motivado pela disciplina Organização e Arquitetura de Computadores II do curso de graduação em Engenharia Elétrica (Ênfase em Computação) da Escola politécnica da Universidade de São Paulo.

## Como utilizar

### Active HDL

A equipe utilizou o Active HDL como ambiente para simulações do porjeto. Porém, como o nosso código é composto de VHDL's sem qualquer dependência de tereeiros, qualquer programa com suporte à linguagem, a exemplo da quartus, pode ser utilizado para simular as hierarquias de memória.

### TopLevel e Tester

Cada hierarquia de memória possui um TopLevel que a conecta com o módulo de teste do projeto, denominada como **Tester** (presente na raíz da pasta src).

Desta maneira para simular o projeto, é necessário, no contexto do topLevel, setar manualmente alguns sinais de entrada, que funcionam com configuração do Tester.

Essencialmente o que este módulo faz é promover a entrada de endereços à hierarquia de memória, em diversos moduos possíveis. Além disso, ele é capaz de detectar stalls providos das hierarquias, tal como um pipeline, e interromper e emissão de endereços até a resolução do miss.

Pedimos que o leitor se dirija à seção 4.4 do relatório para detalhes de como utilizar o tester, pois nesta seção do relatório especificamos a interface deste componente e trazemos casos de uso com imagens apropriadas explicitando como configurar o tester da maneira correta. Dada a sua razoável complexidade, concluímos que o relatório em si seria o host mais apropriado para mostrar estas informações.

## Resumo de Participação

Douglas Ramos (Coordenador)

- Condução de reuniões da equipe, planejamento e gerenciamento do projeto utilizando trello.
- Atuação como facilitador do grupo, resolvendo problemas técnicos de infraestrutura (avtive HDL, git, etc) como também fornecendo auxílio nas implementações e testes de componentes de outros membros, como o cacheL2 e a Memória principal.
- Implementação dos caches de instrução e de dados de ambas hierarquias.
- Revisão dos componentes do projeto e descrição dos memoryHierachy, que integram todos os componentes dentro das hierarquias.

Rafael Higa

- Responsável pela extensa pesquisa teórica de todas as técnicas de otimização, sendo assistido pelo Lucas Kogachi nesta tarefa. Responsável ainda por disseminar o conhecimento apreendido para os integrantes da equipe.
- Implementação de todos os componentes relacionados ao VictimBuffer.
- Implementação do Tester, que é o componente que simula o pipeline e é a peça fundamental na execução dos testes.
- Responsável pela execução e análise dos testes junto com Igor Ortega.

Igor Ortega

- Implementação de todos os componentes relacionados à memória principal, em ambas .
- Implementação de todos os componentes relacionados ao CacheL2.
- Responsável pela execução e análise dos testes junto com Rafael Higa.
- Estudo de melhores abordagens para sincronização entre as partes do sistema.

Lucas Kogachi

- Auxílio na pesquisa das técnicas de otmização.
- Auxílio na implementação dos caches L1.
- Auxílio nos testes.

HenriqueHattori

- Estudo da arquitetura arm, focado principalmente na estrutura das instruções.
- Confeção de cenários de testes utilizando um conjunto de instruções propício e significativo.
- Auxílio na confeção de componentes de integração do sistema.
- Auxílio nos testes.

Todos integrantes ajudaram na cofeção da apresentação e do relatório.

## Estrutura do Projeto

```
src
├── hierarquiBasica      # Pasta contendo todos os componentes da hieraquia Básica e seu topLevel
|   ├──  cacheI                 # top level do Cache de Instruções (Conececta DP + UC)
|   ├──  cacheIPath             # Fluxo de dados do cache de instruções
|   ├──  cacheIControl          # Unidade de controle do cache de instruções
|   ├──  cacheD                 # top level do Cache de Dados (Conececta DP + UC)
|   ├──  cacheDPath             # Fluxo de dados do cache de dados
|   ├──  cacheDControl          # Unidade de controle do cache de dados
|   ├──  memoryL2               # top level da Memória (Conececta DP + UC)
|   ├──  memoryL2Path           # Fluxo de dados da memória
|   ├──  memoryL2Control        # Unidade de controle da memória
|   ├──  memoryHierachy         # Compnenente que integra os componentes da hierarquia
|   ├──  memory.dat             # arquivo .dat com os dados da memória
|   ├──  types                  # tipos específicos definidos para o projeto
|   └──  topLevel               # topLevel que integra esta hierarquia com o tester do projeto
├── hierarquiaOtimizada  # Pasta contendo todos os componentes da hieraquia Básica e seu toLevel
|   ├──  cacheI                 # top level do Cache de Instruções (Conececta DP + UC)
|   ├──  cacheIPath             # Fluxo de dados do cache de instruções
|   ├──  cacheIControl          # Unidade de controle do cache de instruções
|   ├──  cacheD                 # top level do Cache de Dados (Conececta DP + UC)
|   ├──  cacheDPath             # Fluxo de dados do cache de dados
|   ├──  cacheDControl          # Unidade de controle do cache de dados
|   ├──  victimBuffer           # top level do victimBuffer (Conececta DP + UC)
|   ├──  victimBufferPath       # Fluxo de dados do victimBuffer
|   ├──  victimBufferControl    # Unidade de controle do victimBuffer
|   ├──  cacheL1                # Componentenque integra cacheI, cacheD e victimBuffer
|   ├──  cacheL2                # top level do Cache L2 (Conececta DP + UC)
|   ├──  cacheL2Path            # Fluxo de dados do cache L2
|   ├──  cacheL2Control         # Unidade de controle do cache L2
|   ├──  memoryL3               # top level da Memória (Conececta DP + UC)
|   ├──  memoryL3Path           # Fluxo de dados da memória
|   ├──  memoryL3Control        # Unidade de controle da memória
|   ├──  memoryHierachy         # Compnenente que integra os componentes da hierarquia
|   ├──  memory.dat             # arquivo .dat com os dados da memória
|   ├──  types                  # tipos específicos definidos para o projeto
|   └──  topLevel               # topLevel que integra esta hierarquia com o tester do projeto
├── tester               # Componente que simula um pipeline, que se integra às duas hierarquia através de topLevel de cada uma delas
```
