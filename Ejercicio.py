# Paso 1: Definir los Tokens
# Primero, definimos los tokens que nuestro analizador reconocerá:

import re
# Definimos los posibles tokens (números, operadores y paréntesis)
tokens = [
    ("NUM", r"\d+"),  # Números enteros
    ("PLUS", r"\+"),   # Suma
    ("MINUS", r"-"),   # Resta
    ("TIMES", r"\*"),  # Multiplicación
    ("DIVIDE", r"/"),  # División
    ("LPAREN", r"\("), # Paréntesis izquierdo
    ("RPAREN", r"\)"), # Paréntesis derecho
    ("SPACE", r"\s+"), # Espacios (que ignoramos)
]

# Función para tokenizar la entrada
def tokenize(input_string):
    tokens_spec = "|".join(f"(?P<{name}>{pattern})" for name, pattern in tokens)
    regex = re.compile(tokens_spec)
    return [
        (match.lastgroup, match.group())
        for match in regex.finditer(input_string)
        if match.lastgroup != "SPACE"
    ]

# Paso 2: Definir las Funciones Recursivas
# Ahora que tenemos los tokens, implementamos las funciones recursivas. Empezaremos con la función principal, `E`, y luego definiremos las funciones para `T` y `F`:

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else (None, None)

    def eat(self, token_type):
        if self.current_token()[0] == token_type:
            self.position += 1
        else:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token()}")

    # Regla para E -> E + T | E - T | T
    def parse_E(self):
        result = self.parse_T()
        while self.current_token()[0] in ['PLUS', 'MINUS']:
            if self.current_token()[0] == 'PLUS':
                self.eat('PLUS')
                result += self.parse_T()
            elif self.current_token()[0] == 'MINUS':
                self.eat('MINUS')
                result -= self.parse_T()
        return result

    # Regla para T -> T * F | T / F | F
    def parse_T(self):
        result = self.parse_F()
        while self.current_token()[0] in ['TIMES', 'DIVIDE']:
            if self.current_token()[0] == 'TIMES':
                self.eat('TIMES')
                result *= self.parse_F()
            elif self.current_token()[0] == 'DIVIDE':
                self.eat('DIVIDE')
                result /= self.parse_F()
        return result

    # Regla para F -> ( E ) | número
    def parse_F(self):
        if self.current_token()[0] == 'LPAREN':
            self.eat('LPAREN')
            result = self.parse_E()
            self.eat('RPAREN')
            return result
        elif self.current_token()[0] == 'NUM':
            num = int(self.current_token()[1]) 
            self.eat('NUM')
            return num
        else:
            raise SyntaxError(f"Se esperaba número o paréntesis, pero se encontró {self.current_token()}")

# Paso 3: Probar el Analizador
# Ahora podemos probar nuestro analizador con una expresión matemática.
input_string = "3 + 5 * (10 - 4)"
tokenized_input = tokenize(input_string)

parser = Parser(tokenized_input)
result = parser.parse_E()
print(f"Resultado: {result}")
