# Paso 1: Definir los Tokens
# Primero, definimos los tokens que nuestro analizador reconocerá:

import re
from Arbol import TernaryTree

# Definimos los posibles tokens (números, operadores y paréntesis)
tokens = [
    ("NUM", r"\d+"),  # Números enteros
    ("PLUS", r"\+"),  # Suma
    ("MINUS", r"-"),  # Resta
    ("TIMES", r"\*"),  # Multiplicación
    ("DIVIDE", r"/"),  # División
    ("LPAREN", r"\("),  # Paréntesis izquierdo
    ("RPAREN", r"\)"),  # Paréntesis derecho
    ("POWER", r"\^"),   # Exponente
    ("SPACE", r"\s+"),  # Espacios (que ignoramos)
]


# Función para tokenizar la entrada
def tokenize(input_string):
    tokens_spec = "|".join(f"(?P<{name}>{pattern})" for name, pattern in tokens)
    regex = re.compile(tokens_spec)
    tokens_gen = [
        (match.lastgroup, match.group())
        for match in regex.finditer(input_string)
        if match.lastgroup != "SPACE"
    ]
    return tokens_gen


# Paso 2: Definir las Funciones Recursivas
# Ahora que tenemos los tokens, implementamos las funciones recursivas. Empezaremos con la función principal, `E`, y luego definiremos las funciones para `T` y `F`:

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.parse_tree = TernaryTree()
        self.parse_tree.insert('Ei')

    def current_token(self):
        token = self.tokens[self.position] if self.position < len(self.tokens) else (None, None)
        return token

    def eat(self, token_type):
        if self.current_token()[0] == token_type:
            self.position += 1
        else:
            token_actual = self.current_token()
            raise SyntaxError(
                f"Error en posición {self.position}: "
                f"Se esperaba {token_type}, pero se encontró {token_actual}. "
                f"Contexto: {self.tokens[max(0, self.position - 3):self.position + 3]}"
            )

    # Regla para E -> E + T | E - T | T
    def parse_E(self):
        try:
            result = self.parse_T()
            while self.current_token()[0] in ['PLUS', 'MINUS']:
                self.parse_tree.insert('E', "left")
                if self.current_token()[0] == 'PLUS':
                    self.parse_tree.insert('+', "middle")
                    self.eat('PLUS')
                    result += self.parse_T()
                elif self.current_token()[0] == 'MINUS':
                    self.parse_tree.insert('-', "middle")
                    self.eat('MINUS')
                    self.parse_tree.insert('T', "right")
                    result -= self.parse_T()

            self.parse_tree.insert('T', "left")
            return result
        except SyntaxError as e:
            raise SyntaxError(f"Error en 'parse_E': {e}")

    # Regla para T -> T * F | T / F | F
    def parse_T(self):
        try:
            result = self.parse_F()
            while self.current_token()[0] in ['TIMES', 'DIVIDE']:
                if self.current_token()[0] == 'TIMES':
                    self.eat('TIMES')
                    self.parse_tree.insert('*', "middle")
                    result *= self.parse_F()
                elif self.current_token()[0] == 'DIVIDE':
                    self.eat('DIVIDE')
                    self.parse_tree.insert('/', "right")
                    result /= self.parse_F()
            return result
        except SyntaxError as e:
            raise SyntaxError(f"Error en 'parse_T': {e}")

    def parse_F(self):
        try:
            if self.current_token()[0] == 'LPAREN':
                self.eat('LPAREN')
                self.parse_tree.insert('(', "left")
                result = self.parse_E()
                self.eat('RPAREN')
                self.parse_tree.insert(')', "right")
                return result
            elif self.current_token()[0] == 'NUM':
                num = int(self.current_token()[1])
                self.eat('NUM')
                self.parse_tree.insert(f"NUM:{num}", "middle")
                if self.current_token()[0] == 'POWER':
                    self.eat('POWER')
                    exponent = self.parse_F()
                    return num ** exponent
                return num
            else:
                raise SyntaxError(
                    f"Error en posición {self.position}: Token inesperado {self.current_token()}. "
                    f"Se esperaba un número o '('. Contexto: {self.tokens[max(0, self.position - 3):self.position + 3]}"
                )
        except SyntaxError as e:
            raise SyntaxError(f"Error en 'parse_F': {e}")


# Paso 3: Probar el Analizador
# Ahora podemos probar nuestro analizador con una expresión matemática.
input_string = "3 + 5 * (10 - 4)"
tokenized_input = tokenize(input_string)

parser = Parser(tokenized_input)
result = parser.parse_E()
parser.parse_tree.print_tree(parser.parse_tree.root)
print(f"Resultado: {result}")
