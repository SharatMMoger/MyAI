import re
def make_plan(question):
    q = question.lower()
    plan = []
    # File + Read
    if ("find" in q or "open" in q or "read" in q):
        plan.append("search_file")
        plan.append("read_file")
    # Remember
    if "remember" in q:
        plan.append("remember")
    # Calculator
    words = re.findall(r"\b\w+\b", q)
    if any(x in words for x in [
    "add",
    "sum",
    "subtract",
    "multiply",
    "divide",
    "square",
    "cube",
    "power",
    "raised",
    "sqrt",
    "root",
    "percentage"
    ]):
        plan.append("calculator")
    return plan