program VerificaPrimeiraVogal;
var
  nome: string;
  primeiro: char;
begin
  writeln('Digite seu nome:');
  readln(nome);
  if length(nome) = 0 then
  begin
    writeln('String vazia; nenhum car�cter a verificar.');
  end
  else
  begin
    primeiro := nome[1];  
    if (primeiro = 'A') or (primeiro = 'E') or (primeiro = 'I') 
       or (primeiro = 'O') or (primeiro = 'U') then
      writeln('O primeiro car�cter � uma vogal (', nome[1], ').')
    else
      writeln('O primeiro car�cter n�o � uma vogal (', nome[1], ').');
  end;
end.