program ProdutoEscalar;
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
end.