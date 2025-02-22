# Somador

Autor: Pedro de Paula Matos (A103992)

![Foto](../foto.jpg "foto")  
  
Programa que soma todas as sequências de dígitos de um texto (string). Desliga ou liga novamente o comportamento conforme a aparição da string "off"/"on" em qualquer combinação de maiúsculas e minúsculas. Imprime o resultado atual quando encontra o caráter '='. Imprime o total ao finalizar o parsing do texto.

A solução baseia-se num loop que percorre cada caráter do texto enquanto gerencia o estado de ativação através de um booleano. O programa mantém uma variável number para acumular dígitos consecutivos, convertendo-os para inteiros quando encontra um caráter não numérico, adicionando então o inteiro à soma. 