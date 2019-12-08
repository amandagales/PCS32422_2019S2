d11 = {'ldr','ldrb','ldrh','ldrsw','str','sturb','strh',
         'ldtr','ldurb','ldtrh','ldtrsw','sttr','sttrb','sttrh',
         'stxr','stxrb','stxrh','stlxr','stlxrb','stlxrh','adds',
      'sub','subs','eor','orr','cmp','cmn','and','ands','movi','tst', 'ret','adrp'}

d12 = {'ldp','ldpsw','stp','ldnp','stnp','ldxp','stxp','ldaxp','stlxp','movn',
      'asr','adc','adcs','madd','msub','mneg','smull','umull'}

d13 = {'sbc','sbcs','ngc','smaddl','smsubl','smnegl','umaddl','umsubl',
       'umnegl'}

def open_and_clean_txt(file):
    # Abre txt e carrega em uma string
    with open(file, 'r') as f:
        lines = f.read()
    
    # Parte anterior as instrucoes assembly
    pre_texto = lines[0:lines.find(':')+5]
    
    # Instrucoes assembly: Lista de listas: cada lista e uma instrucao com parametros
    aux = lines[lines.find(':')+5:]
    lines = aux[:aux.find('ret')+3].split('\n')
    pos_texto = aux[aux.find('ret')+3:]
    
    # Corrige texto para manipular em string
    new_lines = []
    for i in range(len(lines)):
        if lines[i] != '':
            new_lines.append(lines[i])

    for i in range(len(new_lines)):
        new_lines[i] = new_lines[i].replace('\t',' ',1)
        #new_lines[i] = new_lines[i].replace('[','')
        #new_lines[i] = new_lines[i].replace(']','')
        #new_lines[i] = new_lines[i][new_lines[i].find('\t'):]
        new_lines[i] = new_lines[i].replace('\t',' ').strip()
        new_lines[i] = new_lines[i].split(' ',4)
        
    return new_lines, pre_texto, pos_texto
    
def arm_to_leg(li):
    new_li = []
    for i in range(len(li)):
        # Se for instrucao que mapeia 1:1
        if li[i][0] in d11:
            try:
                y = convert_1_to_1(li[i])
            except:
                y = li[0]
            else:
                new_li.append(y)
        # Se for instrucao que mapeia 1:2
        elif li[i][0] in d12:
            try:
                y1, y2 = convert_1_to_2(li[i])
                new_li.append(y1)
                new_li.append(y2)
            except:
                new_li.append(li[i])
        # Se for instrucao que mapeia 1:3
        elif li[i][0] in d13:
            try:
                y1,y2,y3 = convert_1_to_3(li[i])
                new_li.append(y1)
                new_li.append(y2)
                new_li.append(y3)
            except:
                new_li.append(li[i])
        # instrucao mantem-se
        else:
            new_li.append(li[i])
    return new_li



def convert_1_to_1(x):
    if x[0] == 'ldr':
        x[0] = 'ldur'
        x[2] = x[2]+'#0'
    elif x[0] == 'ldrb':
        x[0] = 'ldurb'
        x[2] = x[2]+'#0'
    elif x[0] == 'ldrh':
        x[0] = 'ldurh'
        x[2] = x[2]+'#0'
    elif x[0] == 'ldrsw':
        x[0] = 'ldursw'
        x[2] = x[2]+'#0'
    elif x[0] == 'str':
        x[0] = 'stur'
        x[2] = +x[2]+'#0'
    elif x[0] == 'strb':
        x[0] = 'sturb'
        x[2] = x[2]+'#0'
    elif x[0] == 'strh':
        x[0] = 'sturh'
        x[2] = x[2]+'#0'
    elif x[0] == 'ldtr':
        x[0] = 'ldur'
    elif x[0] == 'ldtrb':
        x[0] = 'ldurb'
    elif x[0] == 'ldtrh':
        x[0] = 'ldurh'
    elif x[0] == 'ldtrsw':
        x[0] = 'ldursw'
    elif x[0] == 'sttr':
        x[0] = 'stur'
    elif x[0] == 'sttrb':
        x[0] = 'sturb'
    elif x[0] == 'sttrh':
        x[0] = 'sturh'
    elif x[0] == 'stxr':
        x[0] = 'stur'
        x.pop(1)
    elif x[0] == 'stxrb':
        x[0] = 'sturb'
        x.pop(1)
    elif x[0] == 'stxrh':
        x[0] = 'sturh'
        x.pop(1)
    elif x[0] == 'stlxr':
        x[0] = 'stur'
        x.pop(1)
    elif x[0] == 'stlxrb':
        x[0] = 'sturb'
        x.pop(1)
    elif x[0] == 'stlxrh':
        x[0] = 'sturh'
        x.pop(1)
    elif x[0] == 'adds':
        x[0] = 'addis'
    elif x[0] == 'sub':
        x[0] = 'subi'
    elif x[0]== 'subs':
        x[0] = 'subis'
    elif x[0] == 'eor':
        x[0] = 'eori'
    elif x[0] == 'orr':
        x[0] = 'orri'
    elif x[0] == 'cmp':
        x[0] = 'subs'
        x = x[0] + [',WZR'] + x[1:]
    elif x[0] == 'cmn':
        x[0] = 'adds'
        x = x[0] + [',WZR'] + x[1:]
    elif x[0] == 'movi':
        x[0] = 'orr'
        x = x[0] + x[1] + [',WZR'] + x[2:]
    elif x[0] == 'and':
        x[0] = 'andi'
    elif x[0] == 'ands':
        x[0] = 'andis'
    elif x[0] == 'tst':
        x[0] = 'ands'
        x = x[0] + [',WZR'] + x[1:]
    elif x[0] == 'ret':
        if len(x) == 1:
            x[0] = 'br x30'
        else:
            x[0] = 'br'
    elif x[0] == 'adrp':
        x[0] = 'mov'
    
    return x



        
def convert_1_to_2(x):
    if x[0] == 'ldp':
        x1 = ['ldur',x[1],x[3]+'#0']
        if 'w' in x[1].lower():
            x2 = ['ldur',x[2],x[3]+'#4']
        else:
            x2 = ['ldur',x[2],x[3]+'#8']
    
    elif x[0] == 'ldpsw':
        x1 = ['ldursw',x[1],x[3]+'#0']
        x2 = ['ldursw',x[2],x[3]+'#4']
    
    elif x[0] == 'stp':
        x1 = ['stur',x[1],x[3]+'#0']
        x2 = ['stur',x[2],x[3]+'#8']
        
    elif x[0] == 'ldnp':
        x1 = ['ldur',x[1],x[3]]
        x2 = ['ldur',x[2],x[3]]
        
    elif x[0] == 'stnp':
        x1 = ['stur',x[1],x[3]]
        x2 = ['stur',x[2],x[3]]
        
    elif x[0] == 'ldxp':
        x1 = ['ldur',x[1],x[3]]
        x2 = ['ldur',x[2],x[3]]
        
    elif x[0] == 'stxp':
        x1 = ['stur',x[2],x[4]+'#0']
        x2 = ['stur',x[3],x[4]+'#4']
    
    elif x[0] == 'ldaxp':
        x1 = ['ldur',x[1],x[3]]
        x2 = ['ldur',x[2],x[3]]
    
    elif x[0] == 'stlxp':
        x1 = ['stur',x[2],x[4]]
        x2 = ['stur',x[3],x[4]+'#4']
    elif x[0] == 'movn':
        x1 = x
        x2 = ['sub',x[1],'WZR',x[1]]
    elif x[0] == 'asr':
        x1 = ['lsr',x[1],x[2],x[3]]
        x2 = ['addi',x[1],x[1]]
    elif x[0] == 'adc':
        x1 = ['add',x[1],x[2],'HS']
        x2 = ['add',x[1],x[3],x[2]]
    elif x[0] == 'adcs':
        x1 = ['add',x[1],x[2],'HS']
        x2 = ['adds',x[1],x[3],x[1]] 
    elif x[0] == 'madd':
        x1 = ['mul',x[1],x[2],x[3]]
        x2 = ['add',x[1],x[1],x[-1]]
    elif x[0] == 'msub':
        x1 = ['mul',x[1],x[2],x[3]]
        x2 = ['sub',x[1],x[-1],x[1]]
    elif x[0] == 'mneg':
        x1 = ['mul',x[1],x[2],x[-1]]
        x2 = ['sub',x[1],'WZR',x[1]]
    elif x[0] == 'smull':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[-1]]
    elif x[0] == 'umull':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
    
    return x1, x2


def convert_1_to_3(x):
    if x[0] == 'sbc':
        x1 = ['add',x[1],x[2],'HS']
        x2 = ['sub',x[1],x[1],x[3]]
        x3 = ['subi',x[1],x[1],'#1']
    elif x[0] == 'sbcs':
        x1 = ['add',x[1],x[2],'HS']
        x2 = ['sub',x[1],x[1],x[3]]
        x3 = ['subi',x[1],x[1],'#1']
    elif x[0] == 'ngc':
        x1 = ['add',x[1],'WZR','HS']
        x2 = ['sub',x[1],x[1],x[2]]
        x3 = ['subi',x[1],x[1],'#1']
    elif x[0] == 'ngcs':
        x1 = ['add',x[1],'WZR','HS']
        x2 = ['subi',x[1],x[1],'#1']
        x3 = ['subs',x[1],x[1],x[2]]
    elif x[0] == 'smaddl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
        x3 = ['add',x[1],x[1],x[-1]]
    elif x[0] == 'smsubl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
        x3 = ['sub',x[1],x[-1],x[1]]
    elif x[0] == 'smnegl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[-1]]
        x3 = ['sub',x[1],'XZR',x[1]]
    elif x[0] == 'umaddl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
        x3 = ['add',x[1],x[1],x[-1]]
    elif x[0] == 'umsubl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
        x3 = ['sub',x[1],x[-1],x[1]]
    elif x[0] == 'umnegl':
        x1 = ['eor',x[1],x[1],x[1]]
        x2 = ['mul',x[1],x[2],x[3]]
        x3 = ['sub',x[1],'XZR',x[1]]
        
    return x1,x2,x3

def to_string(new_li):
    out = ''
    for i in range(len(new_li)):
        out = out + '        '
        for elem in new_li[i]:
            out = out + elem + ' '
        out += '\n'
    return out

def export_txt(string,arquivo):
    with open(arquivo, "w") as text_file:
        text_file.write(string)
        
        
def main():
    try:
        from tkinter.filedialog import askopenfilename
        print ("Escolha o arquivo com instrucoes ARM")
        arquivo = askopenfilename()
    except:
        arquivo = input("Insira o caminho absoluto do arquivo com as instrucoes ARM: ")
        
    li, pre_texto, pos_texto = open_and_clean_txt(arquivo)
    new_li = arm_to_leg(li)
    string = to_string(new_li)
    string = pre_texto + '\n' + string + pos_texto
    saida = arquivo.replace('.txt','_output.txt')
    export_txt(string, saida)
    print ("Saida gerada em: ", saida)
    
main()
    
    
        
    