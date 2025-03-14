import json
import datetime
import re

STOCK_FILE = "stock.json"
COIN_VALUES = {"1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}

def carregar_stock():
    try:
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_stock(stock):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4)

def listar_produtos(stock):
    print("maq:\ncod | nome | quantidade | preço")
    print("-" * 40)
    for produto in stock:
        print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']}e")

def inserir_moedas(comando, saldo):
    print(comando)
    valores = re.findall(r"(\d+e|\d+c)", comando)
    for val in valores:
        if val in COIN_VALUES:
            saldo += COIN_VALUES[val]
    print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
    return saldo

def selecionar_produto(cod, stock, saldo):
    for produto in stock:
        if produto["cod"] == cod:
            if produto["quant"] == 0:
                print("maq: Produto esgotado")
                return saldo
            preco = int(produto["preco"] * 100)
            if saldo >= preco:
                produto["quant"] -= 1
                saldo -= preco
                print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
            else:
                print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {saldo // 100}c; Pedido = {preco // 100}c")
            return saldo
    print("maq: Produto inexistente")
    return saldo

def calcular_troco(saldo):
    troco = {}
    for moeda, valor in sorted(COIN_VALUES.items(), key=lambda x: -x[1]):
        if saldo >= valor:
            qtd = saldo // valor
            saldo -= qtd * valor
            troco[moeda] = qtd
    return troco

def sair(saldo):
    troco = calcular_troco(saldo)
    if troco:
        troco_str = ", ".join(f"{v}x {k}" for k, v in troco.items())
        print(f"maq: Pode retirar o troco: {troco_str}.")
    print("maq: Até à próxima")

def adicionar_produto(stock):
    cod = input("Digite o código do produto: ")
    nome = input("Digite o nome do produto: ")
    quant = int(input("Digite a quantidade: "))
    preco = float(input("Digite o preço: "))
    for produto in stock:
        if produto["cod"] == cod:
            produto["quant"] += quant
            print("maq: Produto atualizado no stock.")
            return
    stock.append({"cod": cod, "nome": nome, "quant": quant, "preco": preco})
    print("maq: Novo produto adicionado.")

def main():
    stock = carregar_stock()
    print(f"maq: {datetime.date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    saldo = 0
    while True:
        comando = input(">> ").strip()
        if comando == "LISTAR":
            listar_produtos(stock)
        elif comando.startswith("MOEDA"):
            saldo = inserir_moedas(comando, saldo)
        elif comando.startswith("SELECIONAR"):
            cod = comando.split()[-1]
            saldo = selecionar_produto(cod, stock, saldo)
        elif comando == "SAIR":
            sair(saldo)
            break
        elif comando == "ADICIONAR":
            adicionar_produto(stock)
        else:
            print("maq: Comando inválido")
    salvar_stock(stock)

if __name__ == "__main__":
    main()