import math
import re

def calculator():
    print("✨ Unique Expression Solver ✨")
    print("-----------------------------")
    print("Supports pi, e, ^, %, full expressions")
    print("Use '10%4' or '10 % 4' for 10 percent of 4")
    print("Use '2^3 + 10%' for percent of last result")
    print("Type 'exit' to quit")
    print("-----------------------------")

    consts = {
        'pi': math.pi,
        'e': math.e
    }

    while True:
        raw = input("\nexpr: ").strip().lower()
        if raw == 'exit':
            print("bye 👋")
            break

        for key in consts:
            raw = raw.replace(key, str(consts[key]))

        raw = raw.replace('^', '**')

        raw = re.sub(r'(\d+(?:\.\d+)?)\s*%\s*(\d+(?:\.\d+)?)', r'(\1/100 * \2)', raw)

        def percent_replace(match):
            expr_before = match.group(1)
            operator = match.group(2)
            pct = match.group(3)
            return f'({expr_before}){operator}({pct}/100 * ({expr_before}))'

        raw = re.sub(r'(.+?)([\+\-])\s*(\d+(?:\.\d+)?)%', percent_replace, raw)

        raw = re.sub(r'(\d+)%', r'(\1/100)', raw)

        chars = list(raw)
        for i in range(len(chars) - 1):
            if (chars[i].isdigit() and chars[i+1] == '(') or \
               (chars[i] == ')' and chars[i+1].isdigit()) or \
               (chars[i] == ')' and chars[i+1] == '('):
                chars[i] += '*'
        raw = ''.join(chars)

        try:
            val = eval(raw, {"__builtins__": None}, consts)
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            print("Result:", val)
        except ZeroDivisionError:
            print("Can't divide by zero.")
        except SyntaxError:
            print("Syntax issue.")
        except NameError as n:
            print(f"Unknown: {str(n).split()[-1]}")
        except Exception as ex:
            print("Err:", str(ex))

if __name__ == "__main__":
    calculator()
