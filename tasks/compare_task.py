"""
Document comparison task — compares two documents using the LLM.
Usage: "compare file1.pdf and file2.pdf"
"""
import file_tools
from llm_tool import ask_llm


def can_handle(question):
    q = question.lower().strip()
    return q.startswith("compare ") and " and " in q


def read_any_file(filename):
    filename = filename.strip()
    if filename.endswith(".pdf"):
        return file_tools.read_pdf(filename)
    elif filename.endswith(".docx"):
        return file_tools.read_docx(filename)
    elif filename.endswith(".xlsx"):
        return file_tools.read_excel(filename)
    elif filename.endswith(".pptx"):
        return file_tools.read_pptx(filename)
    else:
        return file_tools.read_file(filename)


def run(question, context):
    try:
        content_part = question.strip()[8:]  # remove "compare "
        file1_name, file2_name = content_part.split(" and ", 1)

        file1_content = read_any_file(file1_name)
        file2_content = read_any_file(file2_name)

        prompt = f"""Compare the following two documents and highlight the key differences and similarities.

DOCUMENT 1 ({file1_name.strip()}):
{file1_content}

DOCUMENT 2 ({file2_name.strip()}):
{file2_content}

Provide a clear, structured comparison."""

        return ask_llm(prompt, system_prompt="You are an expert at comparing documents and summarizing differences clearly.")

    except Exception as e:
        return f"Error comparing documents: {str(e)}. Usage: compare file1.pdf and file2.pdf"