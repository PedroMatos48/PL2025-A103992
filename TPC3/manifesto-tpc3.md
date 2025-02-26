# Conversor de Markdown para HTML

Autor: Pedro de Paula Matos (A103992)

![Foto](../foto.jpg "foto")

Este programa transforma texto escrito em formato Markdown em texto HTML. Para tal, recorre a diversas expressões regulares, tanto para determinar o texto a substituir quanto para definir o seu novo formato, e substitui os formatos através de re.sub. 

Conforme o enunciado, o programa apenas converte para os elementos descritos na "Basic Syntax" da Cheat Sheet. Os mais complexos são os cabeçalhos e as listas. A conversão de cabeçalhos é feita através da função convert_headers, que identifica linhas que começam com #, ## ou ###, seguidas de um espaço e do texto do cabeçalho. O número de carácteres '#' determina o nível do cabeçalho HTML (h1, h2, h3). Isso é feito dinamicamente por meio da função len(m.group(1)), que mede a quantidade de carácteres '#' e gera a tag correspondente. 

A conversão de listas numeradas precisa identificar blocos inteiros de itens. Para tal, a função convert_numbered_lists encontra grupos de linhas que seguem o formato 1. Texto, 2. Texto, etc. Após isso, os itens individuais são extraídos e colocados dentro de uma \<ol> (lista ordenada), com cada elemento envolvido por \<li>.

1. [Input em Markdown](input.md)
2. [Output em HTML](output.html)
