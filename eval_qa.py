"""
Evaluation for the document Q&A feature (the `ask` command).

Run from the "My AI" folder, where the PDF is:
    py ".\src 1\eval_qa.py"
"""
from file_tools import read_pdf
from llm_tool import answer_question

PDF_FILE = "cn front page (1).pdf"

# A made-up document with known facts, so answers can be checked exactly.
SAMPLE_DOC = """
Zentra Logistics Pvt Ltd is a freight company headquartered in Pune, India.
It was founded in 2011 by Rahul Mehta.
In the financial year 2024, the company reported revenue of 420 million rupees
and a net profit of 35 million rupees.
Zentra operates warehouses in Pune, Chennai and Hyderabad.
Its main services are road freight, cold storage and last-mile delivery.
The company has a fleet of 180 trucks.
"""

# (document, question, keywords that must appear, is_refusal_test)
# A refusal test asks something that is NOT in the document.
# The correct answer there is that the document does not say.
TESTS = [
    ("sample", "Where is Zentra Logistics headquartered?", ["pune"], False),
    ("sample", "In which year was the company founded?", ["2011"], False),
    ("sample", "Who founded the company?", ["rahul"], False),
    ("sample", "What was the revenue in FY 2024?", ["420"], False),
    ("sample", "How many trucks are in the fleet?", ["180"], False),
    ("sample", "Which cities have warehouses?", ["pune", "chennai", "hyderabad"], False),
    ("sample", "Who is the CEO of the company?", [], True),
    ("sample", "How many employees does the company have?", [], True),
    ("pdf", "What is the course name mentioned in this document?", ["computer networks"], False),
    ("pdf", "Which university is this document from?", ["dayananda sagar"], False),
    ("pdf", "Which academic year is mentioned?", ["2025"], False),
    ("pdf", "Which department is mentioned?", ["computer science"], False),
    ("pdf", "What is the student's USN?", [], True),
]

REFUSAL_PHRASES = [
    "not mention", "no mention", "not contain", "does not", "doesn't",
    "isn't", "is not", "not provided", "not specified", "not state",
    "not found", "no information", "no details", "not available",
    "not include", "not given", "blank", "empty", "not filled",
    "no value", "cannot", "can't", "nahi",
]


def collapse(text):
    return " ".join(str(text).split())


def normalize(text):
    # Models often write curly apostrophes (doesn’t), so convert them to plain ones
    return collapse(text).lower().replace("\u2019", "'").replace("\u2018", "'")


def is_pass(answer, keywords, is_refusal):
    a = normalize(answer)
    if is_refusal:
        return any(phrase in a for phrase in REFUSAL_PHRASES)
    return all(normalize(k) in a for k in keywords)


def main():
    pdf_text = read_pdf(PDF_FILE)
    if pdf_text.startswith("PDF Error"):
        print("Could not read the PDF. Run this from the 'My AI' folder.")
        return

    docs = {"sample": SAMPLE_DOC, "pdf": pdf_text}

    results = []
    for doc_name, question, keywords, is_refusal in TESTS:
        answer = answer_question(docs[doc_name], question)
        ok = is_pass(answer, keywords, is_refusal)
        results.append(ok)

        print(f"[{'PASS' if ok else 'FAIL'}] ({doc_name}) {question}")
        print(f"    {collapse(answer)[:300]}")
        print()

    score = sum(results)
    total = len(results)
    print(f"Score: {score}/{total} ({round(score / total * 100)}%)")


if __name__ == "__main__":
    main()