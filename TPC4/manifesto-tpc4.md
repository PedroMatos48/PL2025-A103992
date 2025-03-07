# Analisador Léxico de Sistema de Queries

Autor: Pedro de Paula Matos (A103992)

![Foto](../foto.jpg "foto")

Este programa lê um determinado tipo de query (SPARQL) e analisa o texto para determinar os diversos tokens que o compõem. Assim, é um analisador léxico. 

Para tal, o código utiliza o módulo ply.lex, definindo os específicos tokens e associando-os a expressões regulares que permitem a sua identificação. 
Os tokens considerados são os seguintes:

- SELECT (e.g.: "select", "?s")
- WHERE ("where", "?w")
- VAR ("?nome", "?desc")
- SHRT ("a")
- LIMIT ("LIMIT")
- URI ("dbo:MusicalArtist", "foaf:name")
- STRING (""Chuck Berry"")
- LANG ("@en")
- NUMBER ("1000")
- AC ("{")
- FC ("}")