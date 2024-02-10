lista_modalidades = set()

total_atletas = 0
total_aptos = 0

escaloes = {}

with open("emd.csv") as f, open("output.txt", "w") as output_file:
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

   
    output_file.write("Modalidades:\n")
    for modalidade in sorted(lista_modalidades):
        output_file.write(f"{modalidade}\n")
        
    output_file.write("\nPercentagens:\n")
    percentagem_apto = round((total_aptos / total_atletas), 2) * 100
    output_file.write(f"Total de Atletas: {total_atletas}\n")
    output_file.write(f"Atletas aptos: {percentagem_apto}%\n")
    output_file.write(f"Atletas inaptos: {100 - percentagem_apto}%\n")
    
    output_file.write("\nEscalões:\n")
    for key in escaloes:
        output_file.write(f"[{key}-{key + 4}]: {escaloes[key]}\n")
