import sys
import re


def process_line(line):
    
    line = re.sub(r'^>(.*)$', r'</blockquote>\1</blockquote>', line) # por em quote
    line = re.sub(r'(### )(.*)',r'<h3>\2</h3>',line) # por em (h3)
    line = re.sub(r'(## )(.*)',r'<h2>\2</h2>',line) # por em (h2)
    line = re.sub(r'(# )(.*)',r'<h1>\2</h1>',line) # por em (h1)
    line = re.sub(r'^(---|\*\*\*|___)$',r'<hr>',line) # por um Horizontal Rule
    line = re.sub(r'(\*\*)(.*)(\*\*)',r'<b>\2</b>',line) # por em bold (**) 
    line = re.sub(r'(\_\_)(.*)(\_\_)',r'<b>\2</b>',line) # por em bold (__)
    line = re.sub(r'(\*)(.*)(\*)',r'<i>\2</i>',line) # por em itálico (*) 
    line = re.sub(r'(\_)(.*)(\_)',r'<i>\2</i>',line) # por em itálico (_)
    line = re.sub(r'.*!\[(.*)\]\((.*)\)',r'<img src="\2" alt="\1"/> ',line) # por em imagem
    line = re.sub(r'.*\[(.*)\]\((.*)\)',r'<a href="\2">\1</a>',line) # por em url
    line = re.sub(r'``(.*)``', r'<code>\1</code>', line) # por em codigo quando é preciso os backticks
    line = re.sub(r'`(.*)`', r'<code>\1</code>', line) # por em codigo numa só linha
    
    
    return line

def recursiveListgeneratorNested(linhas,matriz,indice_atual):

    matriz.append("\t\t<ol>\n")
    matriz[-2] = re.sub(r'(<li>)(.*)(</li>)',r'\1\2',matriz[-2])
    on_list = True
    while on_list:
        line = linhas[indice_atual]
        indice_atual +=1  
        maybe_cont = re.match(r'^(\t|\s{4})\d+\..*',line)
        if(maybe_cont):
            line = re.sub(r'^(\t|\s{4})(\d+\. )(.*)',r'<li>\3</li>',line)
            matriz.append("\t\t\t" + line)
        else:
            on_list = False
    
    matriz.append("\n\t\t</ol>\n\t</li>\n")
    return indice_atual-1
    
def recursiveListGenerator(linhas, matriz, indice_atual):
    matriz.append("<ol>\n")
    on_list = True
    while on_list:
        line = linhas[indice_atual]
        indice_atual +=1  
        maybe_list = re.match(r'^(\t|\s{4})(\d+\.)', line)
        if maybe_list:
            indice_atual = recursiveListgeneratorNested(linhas, matriz,indice_atual-1)
            line = linhas[indice_atual] # tenho que atualizar a linha atual
        else:
            maybe_cont = re.match(r'^(\d+\..*)', line)
            if maybe_cont:
                line = re.sub(r'^(\d+\. )(.*)', r'<li>\2</li>', line)
                matriz.append('\t' + line)
            else:
                on_list = False
    
    matriz.append("\n</ol>\n")
    return indice_atual-1

def recursiveListgeneratorNestedUnsorted(linhas,matriz,indice_atual):

    matriz.append("\t\t<ul>\n")
    matriz[-2] = re.sub(r'(<li>)(.*)(</li>)',r'\1\2',matriz[-2])
    on_list = True
    while on_list:
        line = linhas[indice_atual]
        indice_atual +=1  
        maybe_cont = re.match(r'^(\t|\s{2})[-*+]\s{1}.*', line)
        if(maybe_cont):
            line = re.sub(r'^(\t|\s{2})([-*+]\s{1})(.*)',r'<li>\3</li>',line)
            matriz.append("\t\t\t" + line)
        else:
            on_list = False
    
    matriz.append("\n\t\t</ul>\n\t</li>\n")
    return indice_atual-1

def recursiveListGeneratorUnsorted(linhas, matriz, indice_atual):
    matriz.append("<ul>\n")
    on_list = True
    while on_list:
        line = linhas[indice_atual]
        indice_atual +=1  
        maybe_list = re.match(r'^(\t|\s{2})[-*+]\s{1}.*', line)
        if maybe_list:
            indice_atual = recursiveListgeneratorNestedUnsorted(linhas, matriz,indice_atual-1)
            line = linhas[indice_atual] # tenho que atualizar a linha atual
        else:
            maybe_cont = re.match(r'^[-*+]\s{1}.*', line)
            if maybe_cont:
                line = re.sub(r'^([-*+]\s{1})(.*)', r'<li>\2</li>', line)
                matriz.append('\t' + line)
            else:
                on_list = False
    
    matriz.append("\n</ul>\n")
    return indice_atual-1

  

if len(sys.argv) == 3:
    lines = []
    with open(sys.argv[1]) as in_file: 
        for line in in_file:
            # Guardar as linhas do ficheiro numa lista
            lines.append(line)
    
    with open(sys.argv[2], "w") as output_file:
        output_file.write("<html>\n")
        i = 0  # Initialize the index
        while i < len(lines):
            line = lines[i]
            line = process_line(line)      
            maybe_list = re.match(r'^\d\..*', line)
            maybe_list_un = re.match(r'^[-*+] .*', line)
            listas = []
            if maybe_list:
                listas = []
                i = recursiveListGenerator(lines, listas, i)
                for l in listas:
                    output_file.write(l)
            elif maybe_list_un:
                listas = []
                i = recursiveListGeneratorUnsorted(lines, listas, i)
                for l in listas:
                    output_file.write(l)
            else:
                output_file.write(line)
            i += 1
        output_file.write("\n</html>")