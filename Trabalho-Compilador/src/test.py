ex1 = """program HelloWorld;
begin
    writeln('Ola, Mundo!');
end."""

ex2 = """program Maior3;
var
num1, num2, num3, maior: Integer;
begin
    { Ler 3 números }
    Write('Introduza o primeiro número: ');
    ReadLn(num1);
    Write('Introduza o segundo número: ');
    ReadLn(num2);
    Write('Introduza o terceiro número: ');
    ReadLn(num3);
    { Calcular o maior }
    if num1 > num2 then
        if num1 > num3 then maior := num1
        else maior := num3
    else
        if num2 > num3 then maior := num2
        else maior := num3;
    { Escrever o resultado }
    WriteLn('O maior é: ', maior)
end."""

ex3 = """program Fatorial;
var
    n, i, fat: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(n);
    fat := 1;
    for i := 1 to n do
        fat := fat * i;
    writeln('Fatorial de ', n, ': ', fat);
end."""

ex4 = """program NumeroPrimo;
var
    num, i: integer;
    primo: boolean;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    primo := true;
    i := 2;
    while (i <= (num div 2)) and primo do
        begin
            if (num mod i) = 0 then
                primo := false;
            i := i + 1;
        end;
    if primo then
        writeln(num, ' é um número primo')
    else
        writeln(num, ' não é um número primo')
end."""

ex5 = """program SomaArray;
var
    numeros: array[1..5] of integer;
    i, soma: integer;
begin
    soma := 0;
    writeln('Introduza 5 números inteiros:');
    for i := 1 to 5 do
    begin
        readln(numeros[i]);
        soma := soma + numeros[i];
    end;
    writeln('A soma dos números é: ', soma);
end."""

ex6 = """program BinarioParaInteiro;
var
    bin: string;
    i, valor, potencia: integer;
begin
    writeln('Introduza uma string binária:');
    readln(bin);
    valor := 0;
    potencia := 1;
    for i := length(bin) downto 1 do
    begin
        if bin[i] = '1' then
        valor := valor + potencia;
        potencia := potencia * 2;
    end;
    writeln('O valor inteiro correspondente é: ', valor);
end."""

ex7 = """program BinarioParaInteiro;
function BinToInt(bin: string): integer;
var
    i, valor, potencia: integer;
begin
    valor := 0;
    potencia := 1;
    for i := length(bin) downto 1 do
    begin
        if bin[i] = '1' then
            valor := valor + potencia;
        potencia := potencia * 2;
    end;
    BinToInt := valor;
end;
    
var
    bin: string;
    valor: integer;
begin
    writeln('Introduza uma string binária:');
    readln(bin);
    valor := BinToInt(bin);
    writeln('O valor inteiro correspondente é: ', valor);
end."""


ex8 = """program SomaMediaVetor;
const
  MAX = 5;
var
  v: array[1..MAX] of integer;
  i, soma: integer;
  media: real;
begin
  soma := 0;

  writeln('Digite ', MAX, ' valores inteiros:');
  for i := 1 to MAX do
  begin
    write('v[', i, '] = ');
    readln(v[i]);
    soma := soma + v[i];
  end;

  media := soma / MAX;
  writeln;
  writeln('Soma = ', soma);
  writeln('Média = ', media);
end."""

ex9 = """program VerificaPrimeiraVogal;
var
  nome: string;
  primeiro: char;
begin
  writeln('Digite seu nome:');
  readln(nome);
  if length(nome) = 0 then
  begin
    writeln('String vazia; nenhum carácter a verificar.');
  end
  else
  begin
    primeiro := nome[1];  
    if (primeiro = 'A') or (primeiro = 'E') or (primeiro = 'I') 
       or (primeiro = 'O') or (primeiro = 'U') then
      writeln('O primeiro carácter é uma vogal (', nome[1], ').')
    else
      writeln('O primeiro carácter não é uma vogal (', nome[1], ').');
  end;
end."""

ex10 = """program ProdutoEscalar;
var
  v1, v2: array[1..2] of real;
  i: integer;
  produto: real;
begin
  writeln('Digite ', 2, ' valores reais para o vetor 1:');
  for i := 1 to 2 do
  begin
    write('v1[', i, '] = ');
    readln(v1[i]);
  end;

  writeln;
  writeln('Digite ', 2, ' valores reais para o vetor 2:');
  for i := 1 to 2 do
  begin
    write('v2[', i, '] = ');
    readln(v2[i]);
  end;

  produto := 0.0;
  for i := 1 to 2 do
  begin
    produto := produto + (v1[i] * v2[i]);
  end;

  writeln;
  writeln('O produto escalar de v1 e v2 é: ', produto);
end."""

ex11 = """program AtribuicoesSimples;

var
  x, y: Integer;
  A: array[1..4] of Integer;
  i: Integer;

begin
  x := 10;
  y := 20;

  for i := 1 to 4 do
    A[i] := i * 2;

  Writeln('x = ', x);
  Writeln('y = ', y);
  Writeln('Valores do array A:');
  for i := 1 to 4 do
    Writeln('A[', i, '] = ', A[i]);
end."""