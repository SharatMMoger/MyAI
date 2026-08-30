import re
import math


def detect(question):

    q = question.lower().strip()

    # --------------------------
    # Symbol Operators
    # --------------------------

    m = re.search(r"(\d+)\s*\+\s*(\d+)", q)
    if m:
        return str(float(m.group(1)) + float(m.group(2)))

    m = re.search(r"(\d+)\s*-\s*(\d+)", q)
    if m:
        return str(float(m.group(1)) - float(m.group(2)))

    m = re.search(r"(\d+)\s*\*\s*(\d+)", q)
    if m:
        return str(float(m.group(1)) * float(m.group(2)))

    m = re.search(r"(\d+)\s*/\s*(\d+)", q)
    if m:
        return str(float(m.group(1)) / float(m.group(2)))

    # --------------------------
    # Plus / Minus / Times
    # --------------------------

    m = re.search(r"(\d+)\s+plus\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) + float(m.group(2)))

    m = re.search(r"(\d+)\s+minus\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) - float(m.group(2)))

    m = re.search(r"(\d+)\s+times\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) * float(m.group(2)))

    m = re.search(r"(\d+)\s+divided by\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) / float(m.group(2)))

    # --------------------------
    # Add / Sum
    # --------------------------

    m = re.search(r"add\s+(\d+)\s+and\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) + float(m.group(2)))

    m = re.search(r"sum\s+(?:of\s+)?(\d+)\s+and\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) + float(m.group(2)))

    # --------------------------
    # Subtract
    # --------------------------

    m = re.search(r"subtract\s+(\d+)\s+from\s+(\d+)", q)
    if m:
        return str(float(m.group(2)) - float(m.group(1)))

    # --------------------------
    # Multiply
    # --------------------------

    m = re.search(r"multiply\s+(\d+)\s+by\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) * float(m.group(2)))

    # --------------------------
    # Divide
    # --------------------------

    m = re.search(r"divide\s+(\d+)\s+by\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) / float(m.group(2)))

    # --------------------------
    # Square
    # --------------------------

    m = re.search(r"(\d+)\s+squared", q)
    if m:
        n = float(m.group(1))
        return str(n ** 2)

    m = re.search(r"square\s+of\s+(\d+)", q)
    if m:
        n = float(m.group(1))
        return str(n ** 2)

    # --------------------------
    # Cube
    # --------------------------

    m = re.search(r"(\d+)\s+cubed", q)
    if m:
        n = float(m.group(1))
        return str(n ** 3)

    m = re.search(r"cube\s+of\s+(\d+)", q)
    if m:
        n = float(m.group(1))
        return str(n ** 3)

    # --------------------------
    # Square Root
    # --------------------------

    m = re.search(r"square root of\s+(\d+)", q)
    if m:
        return str(math.sqrt(float(m.group(1))))

    # --------------------------
    # Cube Root
    # --------------------------

    m = re.search(r"cube root of\s+(\d+)", q)
    if m:
        return str(round(float(m.group(1)) ** (1/3), 10))

    # --------------------------
    # Power
    # --------------------------

    m = re.search(r"power\s+(\d+)\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) ** float(m.group(2)))

    m = re.search(r"(\d+)\s+raised to\s+(\d+)", q)
    if m:
        return str(float(m.group(1)) ** float(m.group(2)))

    return None