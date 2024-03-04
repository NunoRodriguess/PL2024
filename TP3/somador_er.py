import sys
import re

current_state = 'ON'
lista_numeros = []

for line in sys.stdin:

    tokens = re.finditer(r'OFF|ON|=|[+\-]?\d+', line,re.IGNORECASE)
    for token in tokens:
        if current_state == 'OFF':
            if token.group().upper() == 'ON':
                current_state = 'ON'
            elif token.group().upper() == 'OFF':
                current_state = 'OFF'
            elif token.group().upper() == '=':
                print(sum(map(int,lista_numeros)))
            else:
                pass
            
        elif current_state == 'ON':
            
            if token.group().upper() == 'ON':
                current_state = 'ON'
            elif token.group().upper() == 'OFF':
                current_state = 'OFF'
            elif token.group().upper() == '=':
                print(sum(map(int,lista_numeros)))
            else:
                lista_numeros.append(token.group())

