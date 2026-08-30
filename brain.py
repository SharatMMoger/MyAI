from memory import save_memory, load_memory
from history import save_history, load_history
from intent import detect_intent
from llm_tool import ask_llm, summarize_text

import file_tools
import math_tools
import sympy_tools
import graph_tools
import conversation
import file_search
import calculator_ai
import nlp_parser
import synonyms
import fuzzy_search
import planner
import entity_parser
import executor
import ast
import conversation_memory
import context_state

from knowledge import knowledge

def get_response(question):
    q = question.lower()
    if "last answer" in q:
        ans = context_state.get_value("last_answer")
        if ans:
            return ans
        return "No previous answer found."
    if "last file" in q:
        f = context_state.get_value("last_file")
        if f:
            return f
        return "No file opened."

    if "summarize it" in q:
        last_file = context_state.get_value("last_file")
        if last_file:
            if last_file.endswith(".pdf"):
                content = file_tools.read_pdf(last_file)
            elif last_file.endswith(".txt"):
                content = file_tools.read_file(last_file)
            elif last_file.endswith(".docx"):
                content = file_tools.read_docx(last_file)
            else:
                content = file_tools.read_file(last_file)
            from llm_tool import summarize_text
            return summarize_text(content)
        return "No file has been opened yet."

    if q.startswith("ask "):
        last_file = context_state.get_value("last_file")
        if not last_file:
            return "No file has been opened yet. Please open a file first."
        question_text = question[4:].strip()
        if last_file.endswith(".pdf"):
            content = file_tools.read_pdf(last_file)
        elif last_file.endswith(".txt"):
            content = file_tools.read_file(last_file)
        elif last_file.endswith(".docx"):
            content = file_tools.read_docx(last_file)
        else:
            content = file_tools.read_file(last_file)
        from llm_tool import answer_question
        return answer_question(content, question_text)
    # Planner
    plan = planner.make_plan(question)
    #print("PLAN :", plan)
    # Executor
    result = executor.execute(plan, question)
    if result:
        return result
    save_history(question)
    question = synonyms.normalize(question)
    #print("DEBUG normalized question:", question)
    conversation_memory.set_question(question)
    memory = load_memory()
    intent = detect_intent(question)
    context_state.set_value("last_intent", intent)
    #print("Intent:", intent)
    entities = entity_parser.extract(question)
    #print(entities)
    parsed = nlp_parser.parse(question)
    if parsed:
                print(parsed)
                if parsed["intent"] == "file_read":
                    keyword = parsed["object"]
                    if keyword.strip() == "":
                        return "Which file do you want to open?"
                    results = file_search.search_file(keyword)
                    if results:
                        filename = results[0]
                        context_state.set_value("last_file", filename)
                        if filename.endswith(".pdf"):
                            return file_tools.read_pdf(filename)
                        elif filename.endswith(".txt"):
                            return file_tools.read_file(filename)
                        elif filename.endswith(".docx"):
                            return file_tools.read_docx(filename)
                        elif filename.endswith(".xlsx"):
                            return file_tools.read_excel(filename)
                        elif filename.endswith(".pptx"):
                            return file_tools.read_pptx(filename)
                        
                    return "No matching file found."
    
    if question == "commands":
        return """
help
list files
read
readpdf
remember
sqrt
power
factorial
gcd
lcm
sin
cos
tan
mean
median
variance
"""
    if question == "history":
        return load_history()

    if question == "history":
        return load_history()

    if question == "last question":
        return str(conversation_memory.get_question())

    if question.lower() == "what was my last question":
        history = load_history().splitlines()

        if len(history) >= 2:
            return history[-2]

        return "No previous question."

    if question.lower() == "repeat":
        return str(conversation_memory.get_answer())

    if question.lower() == "repeat last answer":
        return str(conversation_memory.get_answer())

    if question == "last topic":
        return str(conversation_memory.get_topic())

    if question == "last answer":
        return str(conversation_memory.get_answer())

    if question == "last command":
        return str(conversation_memory.get_command())

    # =====================
    # Conversation Context
    # =====================

    if question == "context":
        return str(conversation_memory.all_context())    

    # =====================
    # File Search
    # =====================
    if question.startswith("find "):
        keyword = question[5:].strip()
        results = file_search.search_file(keyword)

        if not results:
            return "No matching files found."
        return "\n".join(results)
    
    # =====================
    # File Reader
    # =====================

    # List Files
    if question == "list files":
            return file_tools.list_files()

    # Read all txt files
    if question == "read all txt":
        return file_tools.read_all_txt()

    if question.startswith("readpdf "):
        try:
            filename = question.replace("readpdf ", "")
            context_state.set_value("last_file", filename)
            conversation_memory.remember("last_file", filename)
            conversation_memory.set_command("readpdf")
            conversation_memory.set_topic(filename)
            return file_tools.read_pdf(filename)
        except Exception as e:
            return str(e)    

    # Read single file
    if question.startswith("read "):
        try:
            filename = question[5:]
            return file_tools.read_file(filename)
        except Exception as e:
            return str(e)

    if question.startswith("readexcel "):
        try:
            filename = question[10:].strip()
            conversation_memory.remember("last_file", filename)
            conversation_memory.set_command("readexcel")
            conversation_memory.set_topic(filename)
            return file_tools.read_excel(filename)
        except Exception as e:
            return str(e)     

    if question.startswith("readdocx "):
        try:
            filename = question[9:].strip()
            return file_tools.read_docx(filename)
            conversation_memory.remember("last_file", filename)
            conversation_memory.set_command("readdocx")
            conversation_memory.set_topic(filename)
        except Exception as e:
            return str(e)     

    if question.startswith("readppt "):
        try:
            filename = question[8:].strip()
            return file_tools.read_pptx(filename)
            conversation_memory.remember("last_file", filename)
            conversation_memory.set_command("readppt")
            conversation_memory.set_topic(filename)
        except Exception as e:
            return str(e)          

    # =====================
    # Arithmetic
    # =====================

    if question.startswith("sqrt "):
        try:
            number = float(question[5:])
            return str(math_tools.square_root(number))
        except:
            return "Invalid number."

    if question.startswith("power "):
        try:
            parts = question.split()
            base = float(parts[1])
            exponent = float(parts[2])
            return str(math_tools.power(base, exponent))
        except:
            return "Usage: power 2 10"

    if question.startswith("factorial "):
        try:
            number = int(question[10:])
            return str(math_tools.factorial(number))
        except:
            return "Invalid number."

    if question.startswith("gcd "):
        try:
            parts = question.split()
            a = int(parts[1])
            b = int(parts[2])
            return str(math_tools.gcd(a, b))
        except:
            return "Usage: gcd 12 18"

    if question.startswith("lcm "):
        try:
            parts = question.split()
            a = int(parts[1])
            b = int(parts[2])
            return str(math_tools.lcm(a, b))
        except:
            return "Usage: lcm 12 18"

    if question.startswith("percentage "):
        try:
            parts = question.split()
            percent = float(parts[1])
            value = float(parts[2])
            return str(math_tools.percentage(percent, value))
        except:
            return "Usage: percentage 20 500"

    # =====================
    # Trigonometry
    # =====================

    if question.startswith("sin "):
        try:
            angle = float(question[4:])
            return str(round(math_tools.sine(angle), 10))
        except:
            return "Invalid angle."

    if question.startswith("cos "):
        try:
            angle = float(question[4:])
            return str(round(math_tools.cosine(angle), 10))
        except:
            return "Invalid angle."

    if question.startswith("tan "):
        try:
            angle = float(question[4:])
            return str(round(math_tools.tangent(angle), 10))
        except:
            return "Invalid angle."

    # =====================
    # Statistics
    # =====================

    if question.startswith("mean "):
        try:
            numbers = list(map(float, question.split()[1:]))
            return str(math_tools.mean(numbers))
        except:
            return "Usage: mean 10 20 30"

    if question.startswith("median "):
        try:
            numbers = list(map(float, question.split()[1:]))
            return str(math_tools.median(numbers))
        except:
            return "Usage: median 10 20 30"

    if question.startswith("mode "):
        try:
            numbers = list(map(float, question.split()[1:]))
            return str(math_tools.mode(numbers))
        except:
            return "Usage: mode 1 2 2 3"

    if question.startswith("variance "):
        try:
            numbers = list(map(float, question.split()[1:]))
            return str(math_tools.variance(numbers))
        except:
            return "Usage: variance 10 20 30"

    if question.startswith("stddev "):
        try:
            numbers = list(map(float, question.split()[1:]))
            return str(math_tools.stddev(numbers))
        except:
            return "Usage: stddev 10 20 30"

    # =====================
    # Probability
    # =====================

    if question.startswith("ncr "):
        try:
            parts = question.split()
            n = int(parts[1])
            r = int(parts[2])
            return str(math_tools.ncr(n, r))
        except:
            return "Usage: ncr 5 2"

    if question.startswith("npr "):
        try:
            parts = question.split()
            n = int(parts[1])
            r = int(parts[2])
            return str(math_tools.npr(n, r))
        except:
            return "Usage: npr 5 2"

    if question.startswith("probability "):
        try:
            parts = question.split()
            favorable = float(parts[1])
            total = float(parts[2])
            return str(math_tools.probability(favorable, total))
        except:
            return "Usage: probability 3 10"

    # =====================
    # Complex Numbers
    # =====================

    if question.startswith("complex_add "):
        try:
            parts = question.split()
            return str(math_tools.complex_add(parts[1], parts[2]))
        except:
            return "Usage: complex_add 3+4j 1+2j"

    if question.startswith("complex_mul "):
        try:
            parts = question.split()
            return str(math_tools.complex_mul(parts[1], parts[2]))
        except:
            return "Usage: complex_mul 3+4j 1+2j"

    if question.startswith("complex_abs "):
        try:
            value = question.split()[1]
            return str(math_tools.complex_abs(value))
        except:
            return "Usage: complex_abs 3+4j"

    if question.startswith("complex_conj "):
        try:
            value = question.split()[1]
            return str(math_tools.complex_conj(value))
        except:
            return "Usage: complex_conj 3+4j"

    # =====================
    # Vectors
    # =====================

    if question.startswith("vector_add "):
        try:
            content = question[11:]
            parts = content.split("] [")
            v1 = ast.literal_eval(parts[0] + "]")
            v2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.vector_add(v1, v2))
        except:
            return "Usage: vector_add [1,2,3] [4,5,6]"

    if question.startswith("dot "):
        try:
            content = question[4:]
            parts = content.split("] [")
            v1 = ast.literal_eval(parts[0] + "]")
            v2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.dot_product(v1, v2))
        except:
            return "Usage: dot [1,2,3] [4,5,6]"

    if question.startswith("magnitude "):
        try:
            v = ast.literal_eval(question[10:])
            return str(math_tools.magnitude(v))
        except:
            return "Usage: magnitude [3,4]"

    if question.startswith("unit "):
        try:
            v = ast.literal_eval(question[5:])
            return str(math_tools.unit_vector(v))
        except:
            return "Usage: unit [3,4]"

    if question.startswith("cross "):
        try:
            content = question[6:]
            parts = content.split("] [")
            v1 = ast.literal_eval(parts[0] + "]")
            v2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.cross_product(v1, v2))
        except:
            return "Usage: cross [1,2,3] [4,5,6]"
    # =====================
    # Coordinate Geometry
    # =====================

    if question.startswith("distance "):
        try:
            content = question[9:]
            parts = content.split("] [")
            p1 = ast.literal_eval(parts[0] + "]")
            p2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.distance(p1, p2))
        except:
            return "Usage: distance [1,2] [4,6]"

    if question.startswith("midpoint "):
        try:
            content = question[9:]
            parts = content.split("] [")
            p1 = ast.literal_eval(parts[0] + "]")
            p2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.midpoint(p1, p2))
        except:
            return "Usage: midpoint [1,2] [4,6]"

    if question.startswith("slope "):
        try:
            content = question[6:]
            parts = content.split("] [")
            p1 = ast.literal_eval(parts[0] + "]")
            p2 = ast.literal_eval("[" + parts[1])

            return str(math_tools.slope(p1, p2))
        except:
            return "Usage: slope [1,2] [4,6]"

    # =====================
    # SymPy Algebra
    # =====================

    if question.startswith("solve "):
        try:
            expression = question[6:]
            return str(sympy_tools.solve_equation(expression))
        except:
            return "Invalid equation."

    if question.startswith("factor "):
        try:
            expression = question[7:]
            return str(sympy_tools.factor_expression(expression))
        except:
            return "Invalid expression."

    if question.startswith("diff "):
        try:
            expression = question[5:]
            return str(sympy_tools.differentiate(expression))
        except:
            return "Invalid expression."

    if question.startswith("integrate "):
        try:
            expression = question[10:]
            return str(sympy_tools.integrate_expression(expression))
        except:
            return "Invalid expression."

    if question.startswith("simplify "):
        try:
            expression = question[9:]
            return str(sympy_tools.simplify_expression(expression))
        except:
            return "Invalid expression."

    if question.startswith("expand "):
        try:
            expression = question[7:]
            return str(sympy_tools.expand_expression(expression))
        except:
            return "Invalid expression."

    if question.startswith("limit "):
        try:
            expression = question[6:]
            return str(sympy_tools.limit_expression(expression))
        except:
            return "Invalid expression."

    # =====================
    # Matrices
    # =====================

    if question.startswith("det "):
        try:
            matrix_data = ast.literal_eval(question[4:])
            return str(sympy_tools.matrix_determinant(matrix_data))
        except:
            return "Invalid matrix."

    if question.startswith("inverse "):
        try:
            matrix_data = ast.literal_eval(question[8:])
            return str(sympy_tools.matrix_inverse(matrix_data))
        except:
            return "Matrix has no inverse."

    if question.startswith("transpose "):
        try:
            matrix_data = ast.literal_eval(question[10:])
            return str(sympy_tools.matrix_transpose(matrix_data))
        except:
            return "Invalid matrix."

    if question.startswith("matadd "):
        try:
            content = question[7:]
            parts = content.split("]] [[")

            matrix1 = ast.literal_eval(parts[0] + "]]")
            matrix2 = ast.literal_eval("[[" + parts[1])

            return str(sympy_tools.matrix_add(matrix1, matrix2))
        except:
            return "Invalid matrices."

    if question.startswith("matmul "):
        try:
            content = question[7:]
            parts = content.split("]] [[")

            matrix1 = ast.literal_eval(parts[0] + "]]")
            matrix2 = ast.literal_eval("[[" + parts[1])

            return str(sympy_tools.matrix_multiply(matrix1, matrix2))
        except:
            return "Invalid matrices."

    if question.startswith("rank "):
        try:
            matrix_data = ast.literal_eval(question[5:])
            return str(sympy_tools.matrix_rank(matrix_data))
        except:
            return "Invalid matrix."

    if question.startswith("eigen "):
        try:
            matrix_data = ast.literal_eval(question[6:])
            return str(sympy_tools.matrix_eigenvalues(matrix_data))
        except:
            return "Invalid matrix."

    # =====================
    # Polynomial Tools
    # =====================

    if question.startswith("roots "):
        try:
            expression = question[6:]
            return str(sympy_tools.polynomial_roots(expression))
        except:
            return "Invalid polynomial."

    if question.startswith("degree "):
        try:
            expression = question[7:]
            return str(sympy_tools.polynomial_degree(expression))
        except:
            return "Invalid polynomial."

    # =====================
    # Linear System
    # =====================

    if question.startswith("solve2 "):
        try:
            parts = question.split()

            a1 = float(parts[1])
            b1 = float(parts[2])
            c1 = float(parts[3])

            a2 = float(parts[4])
            b2 = float(parts[5])
            c2 = float(parts[6])

            return str(
                sympy_tools.solve_linear_system(
                    a1, b1, c1,
                    a2, b2, c2
                )
            )
        except:
            return "Usage: solve2 2 1 5 1 -1 1"

    # =====================
    # Graphs
    # =====================

    if question.startswith("plot "):
        try:
            expression = question[5:]
            graph_tools.plot_function(expression)
            return "Graph displayed."
        except:
            return "Invalid expression."

    # =====================
    # Memory System
    # =====================

    if question.startswith("remember "):
        try:
            content = question[9:]
            key, value = content.split(" is ", 1)
            save_memory(
            key.strip().lower(),
            value.strip()
            )
            return "I will remember that."
        except:
            return "Usage: remember my name is sharat"
    if question.startswith("what is "):
        key = question[8:].strip().lower()
        if key in memory:
            return memory[key]

    # =====================
    # Knowledge Search
    # =====================

    #import re
    #for key, value in knowledge.items():
        #pattern = r"\b" + re.escape(key.lower()) + r"\b"
        #if re.search(pattern, question.lower()):
            #return value

    reply = conversation.chat(question)
    if reply:
        conversation_memory.set_answer(reply)
        return reply

    answer = calculator_ai.detect(question)
    if answer:
        conversation_memory.set_answer(answer)
        return answer

    llm_answer = ask_llm(question)
    conversation_memory.set_answer(llm_answer)
    return llm_answer