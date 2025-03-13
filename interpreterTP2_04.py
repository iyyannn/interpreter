class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return ('INTEGER', self.integer())

            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            
            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')
            
            if self.current_char == '*':
                self.advance()
                return ('MUL', '*')
            
            if self.current_char == '/':
                self.advance()
                return ('DIV', '/')

            self.error()
        
        return ('EOF', None)

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat('INTEGER')
        return token[1]

    def term(self):
        result = self.factor()

        while self.current_token[0] in ('MUL', 'DIV'):
            token = self.current_token
            if token[0] == 'MUL':
                self.eat('MUL')
                result *= self.factor()
            elif token[0] == 'DIV':
                self.eat('DIV')
                result /= self.factor()
        
        return result

    def expr(self):
        self.current_token = self.get_next_token()
        result = self.term()

        while self.current_token[0] in ('PLUS', 'MINUS'):
            token = self.current_token
            if token[0] == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif token[0] == 'MINUS':
                self.eat('MINUS')
                result -= self.term()

        return result


def main():
    while True:
        try:
            text = input('calc> ')
            if not text:
                continue
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()