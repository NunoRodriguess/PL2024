import ply.lex as lex
import json
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
            "1c": 1,
            "2c": 2,
            "5c": 5,
            "10c": 10,
            "20c": 20,
            "50c": 50,
            "1e": 100,
            "2e": 200
        }
        return coin_values[coin_str]
        

    def t_receber_MOEDAS(self,t):
        r'[125]c|[125]0c|[12]e'
        x = self.moedas[t.value]
        self.moedas[t.value] = x + 1
        self.saldo += (self.parse_coin_value(t.value) / 100)
        self.saldo = round(self.saldo,2)
        euros = int(self.saldo)
        cents = int((self.saldo - euros) * 100) 
        print(f"maq: Saldo =  {euros}e{cents:02}c")

        return t
    def generate_change_line(self):

        troco = self.saldo
        coins_to_return = []
        
        coin_denominations = ["2e","1e", "50c", "20c", "10c", "5c", "2c", "1c"] # ordem é importante!
        
        for coin in coin_denominations:
            count = self.moedas.get(coin, 0)
            
        
            num_coins = min(count, (troco * 100) // (self.parse_coin_value(coin)))
            troco = troco * 100
            troco -= num_coins * (self.parse_coin_value(coin))
            troco = troco / 100
            if num_coins == 0:
                pass
            else:
                coins_to_return.append(f"{int(num_coins)}x {coin}")
                self.moedas[coin] = count - num_coins
 
        if round(troco,2) == 0:
            output = "maq: Pode retirar o troco:"
            output += ", ".join(coins_to_return) + "."
        else:
            output = "maq: Troco não pode ser devolvido, contacte o apoio ao cliente."
    
        return output

    
    def t_selecionar_ID(self,t):
        r'[a-zA-Z]\d+'
        try:
            preco = float(self.produtos[t.value.upper()][1])
            
            if (self.saldo < preco):
                print(f"maq: Saldo insufuciente para satisfazer o seu pedido")
                euros_s = int(self.saldo)
                cents_s = int((self.saldo - euros_s) * 100)
                euros_p = int(preco)
                cents_p = int((preco - euros_p) * 100)
                print(f"maq: Saldo = {euros_s}e{cents_s:02}c; Pedido = {euros_p}e{cents_p:02}c")
                self.lexer.begin('receber')
                # baixar o stock
            elif int(self.produtos[t.value.upper()][2]) <=0:
                print(f"maq: Sem stock de {self.produtos[t.value.upper()][0]}")
                self.lexer.begin('receber')
            else:
                self.saldo -= preco
                self.saldo = round(self.saldo,2)
                self.lexer.begin('receber')
                print(f"maq: Pode retirar o produto dispensado \"{self.produtos[t.value.upper()][0]}\"")
                euros = int(self.saldo)
                cents = int((self.saldo - euros) * 100)
                print(f"maq: Saldo =  {euros}e{cents:02}c")
        except:
           print(f"maq: Id não válido")
           self.lexer.begin('receber') 
        return t
    
    def t_receber_SAIR(self,t):
        r'[Ss][Aa][iI][Rr]'
        
        pt = self.generate_change_line()
        print(pt)
        sys.exit(0) 
        return t
    
    def print_produtos(self):
        print("cod | nome | quantidade | preço")
        print("-" * 35)  # Separator line
        
        for _id, (nome, quantidade, preco) in self.produtos.items():
            if _id == "id":
                continue  # Skip the header row
            print(f"{_id} | {nome} | {quantidade} | {preco}")

        
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
        self.moedas = {
                "2e": 10,
                "1e": 20,
                "50c": 26,
                "20c": 43,
                "10c": 24,
                "5c": 30,
                "2c": 10,
                "1c": 33
        }
        with open('stock.json', 'r') as fcc_file:
            fcc_data = json.load(fcc_file)
            for item in fcc_data['stock']:
                self.produtos[item['cod']] = (item['nome'], item['preco'], item['quant'])
        
                    
        
    
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