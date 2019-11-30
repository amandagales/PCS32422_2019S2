# Unidade funcional compatível IEEE 754 - Grupo I

- Felipe Coelho de Abreu Pinna Nº USP 9837177
- Gabriel Takeshi Medeiros Yamasaki Nº USP 9837538
- Ian Alkmin Santos La Rosa Nº USP 9837271
- Victor Passos de Pinho Nº USP 9426731

## Descrição

Este trabalho teve como objetivo produzir uma unidade funcional
de operações com número em formato de ponto flutuante de acordo
com o padrão IEEE 754. Foram implementadas as operações usadas
pelo conjunto de instruções do LEGv8, que são apenas as funçoes
necessárias para o processador do projeto.

## Infraestrutura necessária

Nenhum programa específico é necessário para a simulação do projeto, qualquer ferramenta de síntese de VHDL e de simulação de VHDL pode ser utilizada. Porém o arquivo providenciado é do tipo projeto arquivado do Quartus (.qar), logo o uso desta ferramenta facilita o processo. Para simulação foi utilizado pelo grupo o Aldec Active-HDL, pois providencia fácil visualização dos resultados, porém qualquer outra ferramenta, como o ModelSim, pode ser utilizada.

## Instruções para simulação

Antes de compilar e sintetizar o projeto atente ao arquivo ‘testbench.vhd’, a simulação é regida por este componente. O testbench opera como uma simples máquina de estado, possuindo cinco estados principais, e realiza duas operações seguidas (esperando a conclusão da primeira para executar a segunda), caso for necessário executar mais operações basta apenas copiar e colar mais um estado na máquina com o mesmo formato dos dois presentes (existe um estado intermediário entre operações que preenche todas as saídas com 0s , mas não é necessária, está presente apenas para melhor clareza dos resultados na simulação). Para modificar as operações simuladas, basta alterar o valor dos campos no estado, X1 e X2 são os operadores, escritos em formato ponto flutuante e representados em hexadecimal ( recomendo o uso dos sites binaryconvert.com/convert_float.html , e binaryconvert.com/convert_double.html para a conversão de números de ponto flutuante de decimal para hexadecimal, e vice-versa ), ‘opcode’ é o campo da operação a ser realizada e ‘shamt’ seu respectivo shamt, seus valores estão no relatório do projeto ( quando for realizar operações de precisão single, por favor zerar a metade mais significativa do campo dos operadores X1 e X2 ).

Tendo as operações que deseja simular escritas propriamente, basta apenas realizar a análise e síntese do Quartus e abrir a ferramenta de simulação. Existem vários sinais que podem ser acompanhados na simulação (descrição de todos está no relatório), porém recomendo a visualização apenas de alguns sinais do componente ‘testbench’, entre eles o sinal de clock ‘clk’, o bus de entrada de dados ‘data’, o sinal de operação finalizada ‘done’, o bus dos códigos de condição ‘cc’, e o bus do resultado final ‘res’. Observando esses sinais é possível verificar quando uma operação é enviada, o fim desta operação e seu resultado e flags de estado setadas.
