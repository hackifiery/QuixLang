import sys
import re

class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, code):
        tokens = code.split()
        if tokens[0] == 'set':
            variable = tokens[1]
            expression = ' '.join(tokens[2:])
            result = self.evaluate_expression(expression)
            self.variables[variable] = result
        elif tokens[0] == 'get':
            variable = tokens[1]
            if variable in self.variables:
                return self.variables[variable]
            else:
                raise Exception(f"Variable '{variable}' not found.")
        elif tokens[0] == 'display':
            if len(tokens) >= 2 and ((tokens[1].startswith('"') and tokens[-1].endswith('"')) or (tokens[1].startswith("'") and tokens[-1].endswith("'"))):
                output = ' '.join(tokens[1:])[1:-1]
                print(output)
            else:
                for token in tokens[1:]:
                    if token in self.variables:
                        result = self.variables[token]
                        if isinstance(result, str):
                            print(result)
                        else:
                            print(f"{token} = {result}")
                    else:
                        try:
                            result = self.evaluate_expression(token)
                            print(f"{token} = {result}")
                        except:
                            print(f"Variable '{token}' not found.", file=sys.stderr)
        elif tokens[0] == 'if':
            condition = self.evaluate_expression(tokens[1])
            if condition:
                self.eval(' '.join(tokens[2:]))
        elif tokens[0] == 'while':
            condition = self.evaluate_expression(tokens[1])
            while condition:
                self.eval(' '.join(tokens[2:]))
                condition = self.evaluate_expression(tokens[1])
        elif tokens[0] == 'for':
            variable = tokens[1]
            start = int(tokens[3])
            end = int(tokens[5])
            step = int(tokens[7])
            for i in range(start, end, step):
                self.variables[variable] = i
                self.eval(' '.join(tokens[8:]))
        elif tokens[0] == 'solve':
            expression = ' '.join(tokens[1:])
            result = self.evaluate_expression(expression)
            print(result)
        else:
            raise Exception("Invalid command.")

    def evaluate_expression(self, expression):
        # Replace variable names with their values
        expression = re.sub(r'\b\w+\b', lambda match: str(self.variables.get(match.group(0), match.group(0))), expression)
        # Evaluate the expression using eval
        return eval(expression, {}, self.variables)

def shell():    
    # Interactive shell
    interpreter = Interpreter()

    while True:
        user_input = input(">>> ")
        if user_input == 'exit':
            break
        try:
            interpreter.eval(user_input)
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
