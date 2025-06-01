from PascalYacc import parser
from test import ex1, ex2, ex3, ex4, ex5, ex6,ex7, ex8, ex9, ex10, ex11
from ASTInterpreter import ASTInterpreter
import pprint

if __name__ == "__main__":
    print("Qual exemplo quer testar:")
    print("""
1: Hello World!
2: Maior Numero entre 3
3: Fatorial
4: NumeroPrimo
5: SomaArray
6: BinarioParaInteiro
7: --------------
8: SomaMediaVetor
9: VerificaPrimeiraVogal
10: ProdutoEscalar
11: AtribuicoesSimples
    """)
    choice = input()
    while not choice.isdigit() or int(choice) not in [1,2,3,4,5,6,8,9,10,11]:
        print("Escolha Inválida, escolha um dos numeros válidos")
        choice = input()
    ex = ""
    match(choice):
        case "1":
            ex = ex1
        case "2":
            ex = ex2
        case "3":
            ex = ex3
        case "4":
            ex = ex4
        case "5":
            ex = ex5
        case "6":
            ex = ex6
        case "8":
            ex = ex8
        case "9":
            ex = ex9
        case "10":
            ex = ex10
        case "11":
            ex = ex11
    print("Este é o codigo em Pascal")
    print(ex)
    print("Enter para continuar")
    input()

    ast = parser.parse(ex)
    interp = ASTInterpreter()
    interp.interpret(ast)
    interp.run()