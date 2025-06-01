program SomaMediaVetor;
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
end.