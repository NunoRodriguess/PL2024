import ply.lex as lex
import csv
import sys

class VendingMachine(object):
    # List of token names.   This is always required
    tokens = (
       'ID',
       'SAIR',
       'SELECIONAR',
       'LISTAR',
       'MOEDAS'
    )
    states = (
        ('selecionar','inclusive'),
        ('receber','inclusive'),
    )

    def parse_coin_value(self,coin_str):
        coin_values = {
            "5c": 5,
            "10c": 10,
            "20c": 20,
            "50c": 50,
            "1e": 100,
            "2e": 200
        }
        return coin_values[coin_str]
        

    def t_receber_MOEDAS(self,t):
        r'5c|[125]0c|[12]e'
        self.saldo += self.parse_coin_value(t.value)
        print(f"SALDO: {self.saldo}c")
        return t
    
    def t_selecionar_ID(self,t):
        r'\d+'
        preco = self.produtos[t.value][1]
        split = preco.split('c')
        self.saldo -= int(split[0])
        self.lexer.begin('receber')
        print(f"SALDO: {self.saldo}c")
        return t
    
    def t_receber_SAIR(self,t):
        r'[Ss][Aa][iI][Rr]'
        print(f"TROCO: {self.saldo}c")
        sys.exit(0) 
        return t
    
    def print_produtos(self):
        for _id in self.produtos.keys():
            if _id =="id":
                pass
            else:
                tup = self.produtos[_id]
                print(f"{_id} {tup[0]} {tup[1]}")
        
    def t_receber_LISTAR(self,t):
        r'[lL][iI][sS][tT][Aa][Rr]'
        self.print_produtos() 
        return t
    
    def t_receber_SELECIONAR(self,t):
        r'[sS][eE][lL][eE][cC][iI][oO][nN][Aa][Rr]'
        self.lexer.begin('selecionar')
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.begin('receber')
    
    def __init__(self):
        self.produtos = {}
        self.saldo = 0 # em centimos
        with open('stock.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                    self.produtos[lines[0]] = lines[1],lines[2]
        
    
    # Test it output
    def run(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             

# Build the lexer and try it out
v = VendingMachine()
v.build()       
    
for line in sys.stdin:
    v.run(line)     