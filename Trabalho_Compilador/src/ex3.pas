program Fatorial;
var
    n, i, fat: integer;
begin
    writeln('Introduza um n�mero inteiro positivo:');
    readln(n);
    fat := 1;
    for i := 1 to n do
        fat := fat * i;
    writeln('Fatorial de ', n, ': ', fat);
end.