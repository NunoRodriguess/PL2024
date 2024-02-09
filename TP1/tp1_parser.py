lista_modalidades = set()

total_atletas = 0
total_aptos = 0

escaloes = {} # chaves é o mod 5 para as fichas etárias
              # e.g 3 mod 5 = 3, o que 3 - 3 = 0, logo a chave é 0.
              # e.g 22 mod 5 = 2, o que 22 - 2 = 20, logo a chave é 20

#com o import sys
#for line in sys.stdin:
#... mesma lógica
# optei por ler e escrever para um ficheiro

with open("emd.csv") as f:
    
    for line in f:
        if line != "_id,index,dataEMD,nome/primeiro,nome/último,idade,género,morada,modalidade,clube,email,federado,resultado\n":   
            colunas = line.split(',')
            
            #tratar modalidades
            lista_modalidades.add(colunas[8])
            
            #tratar aptidao
            if 'true' in colunas[12]:
                total_aptos += 1
            total_atletas += 1
            
            #tratar escalão
            idade = int(colunas[5])
            resto = idade % 5
            chave = idade - resto
            
            atletas_do_escalao = escaloes.pop(chave, 0)
            escaloes[chave] = atletas_do_escalao + 1
        
        
        
        

# transformar set numa lista, ordenar e mostrar 
lista_modalidades = list(lista_modalidades)
lista_modalidades.sort()
print(lista_modalidades)

print(" ")
# mostrar percentagens

percentagem_apto = round((total_aptos / total_atletas), 2) * 100
print(f'"Total de Atletas: {total_atletas} %"')
print(f'"Atletas aptos: {percentagem_apto} %"')
print(f'"Atletas inaptos: {100 - percentagem_apto} %"')

print(" ")
#mostrar escaloes

def gera_escalao(primeiro):
    return f'"[{primeiro}-{primeiro + 4}]: {escaloes[primeiro]}"'

for key in escaloes:
    print(gera_escalao(key))

print(" ")


