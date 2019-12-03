# PCS32422_2019S2 - Grupo G - Scoreboard

Gabriel Henrique Justino Ribeiro 9837733

Gabriela von Staa Guedes 9853248 

Luana Vicente Leite 9281074

Michel Chieregato 9042790

Na nossa branch, temos duas pastas (C e VHDL) e o relatório. 


A src da C contém o arquivo principal ArmEmulator.c. As instruções de teste estão dentro do arquivo (linhas 1330 a 1340), caso queira mudar o set de instruções deve-se alterar no código diretamente. A inserção dos valores iniciais na memória também é feito dentro do código (linhas 1299 a 1306). Deve-se compilar com gcc e rodar o arquivo criado.


A pasta VHDL tem todos os arquivos do processador, mas os relevantes para o projeto são a UC (unidade_de_controle.vhd) e o testbench (testbench_scoreboard.vhd). Para testar, deve abrir o projeto no Quartus ou Active e selecionar como top-level o arquivo de testbench.


No relatório, explicamos o processo de desenvolvimento tanto do C quanto do VHDL, os testes feitos para cada e as falhas no projeto final. Como resumo: escolhemos um emulador em C do Arm v8 (link do repositório original no relatório), alteramos o código para conter a lógica de scoreboard e, quando completo, tentamos traduzir para VHDL. Seguimos pela linha da lógica mas sem fazer uma tradução ponto a ponto, chegando a um código VHDL com a lógica completa mas com alguns erros, como é possível ver nos waveforms do relatório.


Sobre a participação de cada integrante, tentamos dividir em duplas: a Gabriela e o Michel ficaram com o desenvolvimento em C e, depois de finalizado, a Luana e o Gabriel iniciaram o código em VHDL. Apesar dessa divisão, todos participaram de cada etapa, sendo com pesquisa, opiniões e inclusive escrita de código.


Em qualquer necessidade de contato, por favor enviar e-mail para luana.vicente.leite@usp.br (coordenadora).


