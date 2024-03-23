# Gramática _LL(1)_

Autor: Jorge Nuno Gomes Rodrigues,A101758

Neste trabalho começei por escrever uma gramática que conseguisse capatar as regras presentes na aritmética que nós conhecemos. Nesse aspeto, a primeira versão foi um sucesso, mas não suportava outras capacidades requisitadas para o projeto, isto é, ser uma gramática _LL(1)_. Neste caso em particular, havia muitas ocurrências onde os lookaheads das produções eram exatamente iguais.

Na segunda etapa, optei por resolver os problemas da gramática anterior com uma estratégia de subsituição por um simbolo não terminal extra, algo comum em problemas first/first. O resultado, assim como a primeira versão, serviram para representar exprossões aritméticas, mas por motivos semlhantes, certas produções possuiam exemplos em comum como exemplificado no documento.

Finalmente, reparei que o problema, na verdade, não era um caso normal de first/first, mas sim um caso especial chamado de _recursão à esquerda_. Deste modo, apliquei a forma standard de remoção de recursão à esquerda que levou à versão final. Esta gramática já era capaz de traduzir todos os requisitos do TPC6