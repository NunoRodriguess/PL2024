# Primeiro Parser
Autor: Jorge Nuno Gomes Rodrigues,A101758<br />

Primeiro programa desenvolvido a pedido da disciplina. Apenas realiza as estatísticas pedidas,mas decidi exprimentar usar, uma abordagem de ficheiros, e uma abordagem que utiliza o stdin e stdout.<br />
A solução é simples: Primeiramente decidi utilizar 3 estruturas de dados: um conjunto para guardar as modalidades; dois valores inteiros para contar utilizadores e finalmente um mapa que guarda as fases etárias, usando como chave o primeiro valor por fase, e.g, [30-34] usa chave 30, e como valor o total.

A nível de lógica, por linha, adiciono ao conjunto a modalidade (não permite repetições); caso o atleta esteja apto, conto um, caso não esteja, não conto (contando sempre um no total);Adiciono sempre mais um ao valor ao valor atual dependendo escalão do atleta.

Finalmente, apenas é preciso converter o conjunto para lista e ordenar alfabéticamente; Calcular as percentagens da aprovação e finalmente mostrar o dicionário final.