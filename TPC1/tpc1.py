def sum_integers_from_text(text):
    total = 0
    number = ''
    active = True  
    
    i = 0
    while i < len(text):
        char = text[i]
        
        if text[i:i+2].lower() == "on":
            active = True
            i += 1  
        elif text[i:i+3].lower() == "off":
            active = False
            i += 2  
        elif char == "=":
            print("Soma atual:", total)  
        elif active and char.isdigit():
            number += char  
        else:
            if number:
                total += int(number)  
                number = ''  
        
        i += 1
    
    if number:  
        total += int(number)
    
    print("Resultado final:", total)

if __name__ == "__main__":
    import sys
    print("Escreva um texto (pressione Ctrl+D para terminar o input em Unix/macOS ou Ctrl+Z em Windows):")
    input_text = sys.stdin.read()
    sum_integers_from_text(input_text)