"""
Calculator task — handles basic arithmetic commands like sqrt, power.
"""
import math_tools

def can_handle(question):
    q = question.lower().strip()
    keywords = ["sqrt ", "power ", "factorial ", "gcd ", "lcm ", "percentage "]
    return any(q.startswith(k) for k in keywords)

def run(question, context):
    q = question.lower().strip()

    if q.startswith("sqrt "):
        try:
            number = float(q[5:])
            return str(math_tools.square_root(number))
        except:
            return "Invalid number."

    if q.startswith("power "):
        try:
            parts = q.split()
            base = float(parts[1])
            exponent = float(parts[2])
            return str(math_tools.power(base, exponent))
        except:
            return "Usage: power 2 10"

    if q.startswith("factorial "):
        try:
            number = int(q[10:])
            return str(math_tools.factorial(number))
        except:
            return "Invalid number."

    if q.startswith("gcd "):
        try:
            parts = q.split()
            return str(math_tools.gcd(int(parts[1]), int(parts[2])))
        except:
            return "Usage: gcd 12 18"

    if q.startswith("lcm "):
        try:
            parts = q.split()
            return str(math_tools.lcm(int(parts[1]), int(parts[2])))
        except:
            return "Usage: lcm 12 18"

    return None

def verify(question, result):
    """
    A calculator result is genuinely successful only if it's a valid number
    (not an error message).
    """
    try:
        float(result.strip())
        return True
    except (ValueError, AttributeError):
        return False 