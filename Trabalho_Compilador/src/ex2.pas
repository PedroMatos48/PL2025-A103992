program Maior3;
var
num1, num2, num3, maior: Integer;
begin
    { Ler 3 n�meros }
    Write('Introduza o primeiro n�mero: ');
    ReadLn(num1);
    Write('Introduza o segundo n�mero: ');
    ReadLn(num2);
    Write('Introduza o terceiro n�mero: ');
    ReadLn(num3);
    { Calcular o maior }
    if num1 > num2 then
        if num1 > num3 then maior := num1
        else maior := num3
    else
        if num2 > num3 then maior := num2
        else maior := num3;
    { Escrever o resultado }
    WriteLn('O maior �: ', maior)
end.