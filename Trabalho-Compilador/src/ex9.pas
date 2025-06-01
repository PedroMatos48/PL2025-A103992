program VerificaPrimeiraVogal;
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
end.