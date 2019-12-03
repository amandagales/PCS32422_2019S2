# Barramento AMBA

## Descrição
O presente projeto teve o objetivo de implementar um barramento, uma interface de conexão entre mestres e escravos, que são módulos que utilizam do barramento para fazerem transferências entre si. O barramento construído permite a conexão de até 4 mestres e 16 escravos.


Para que essa conexão seja realizada com sucesso, alguns outros componentes são essenciais, como o árbitro, para mediar o acesso dos mestres ao barramento. O árbitro, por sua vez, é composto por quatro elementos: multiplexador, registrador, demultiplexador e o masterselector. Já o barramento, é composto de um multiplexador e um decodificador. Mais detalhes podem ser vistos pelo relatório. 


## Instruções

### Testes e simulações
O projeto foi desenvolvido e testado no software Quartus Prime Lite.


Foram desenvolvidos duas entidades TopLevel: uma denomina-se apenas “TopLevel” e a outra “TopLevelv2”. A primeira possui algumas entradas e saídas de teste, para simulação, enquanto que a segunda possui apenas as entradas de HCLK e HRESETn.


Os testes são feito com WaveForms, sendo que alguns já foram enviados junto ao código.
Na entidade TopLevel de teste foram colocadas entradas para simulações de dois mestres, sendo 4 escravos instanciados (os escravos possuem uma máquina de estados que simulam seu comportamento. Os mestres devem ser ter comportamento simulado pelo usuário): 
- “HADDR_teste_M0” e “HADDR_teste_M1”: são os sinais de endereço dos mestres 0 e 1 e são usados para acessar um dado endereço de um dado escravo. Vale lembrar que como há 16 conexões possíveis com escravos, o algoritmo de decodificação escolhido se baseia nos 4 primeiros bits do endereço. Vale ressaltar que foram instanciados 4 escravos, com a máquina de estados descrita no relatório. 
- “HTRANS_teste_M0” e “HTRANS_teste_M1” indicam se está ocorrendo ou não transferência para dado mestre. É um sinal de dois bits, cujo bit mais significativo indica que há transferência (existem 2 tipos de transferência, denotadas por “10” e “11”, mas são tratadas da mesma forma pelo barramento).
- HWRITE_teste: sinal que indica se a operação sendo feita é de escrita (‘1’) ou leitura (‘0’). 


Os sinais de saída foram (Nos testes realizados, testou-se o uso dos escravos ‘0’ e ‘2’, por isso apenas estes sinais foram instanciados, mas pode-se colocar como saída os sinais de quaisquer escravos instanciados):
“HREADYOUT_0” e “HREADYOUT_2”: sinais de saída que indicam se o escravo está pronto para novas operações. Devido ao modo como a máquina de estados do escravo foi desenvolvida, a variação do valor deste sinal indica que este escravo está sendo acessado.
“HRDATAOUT”: barramento de dados conectado aos mestres com os dados acessados. 
“HSEL1_OUT” e “MuxSelect1_OUT” são sinais intermediários usados para comprovar o comportamento desejado.


Portanto, para testes já na configuração fornecida, basta definir os valores das entradas, simulando os mestres a partir da variação dos sinais conforme o comportamento a ser constatado. 
Para um número maior ou menor de mestres e escravos, basta adaptar as entradas e saídas e os portmaps dos componentes, que são limitados a 4 mestres e 16 escravos. Para o caso de haver menos mestres e escravos, as entradas dos componentes referentes a mestres e escravos não presentes são deixadas sempre em ‘0’ e as saídas são deixadas em aberto. (No arquivo de teste, essa foi a configuração).


Para testes de outros mestres e escravos, basta, para os mestres, incluir o componente com entradas e saídas correspondentes dentro do componente “master” e para os escravos, deve-se fazer o mesmo, além de excluir os trechos de código VHDL dentro da architecture, visto que esta é a máquina de estados usada para teste.



## Authors

Giovanni Abeni

Guilherme Vecchi

João Lins

Lucas Pereira

Thábata Pontes