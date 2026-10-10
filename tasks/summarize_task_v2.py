"""
Summarize task — summarizes the last opened file using the LLM.
"""
import file_tools
import context_state
from llm_tool import summarize_text


def can_handle(question):
    q = question.lower().strip()
    return "summarize it" in q or q == "summarize"


def run(question, context):
    last_file = context_state.get_value("last_file")

    if not last_file:
        return "No file has been opened yet."

    try:
        if last_file.endswith(".pdf"):
            content = file_tools.read_pdf(last_file)
        elif last_file.endswith(".docx"):
            content = file_tools.read_docx(last_file)
        elif last_file.endswith(".xlsx"):
            content = file_tools.read_excel(last_file)
        elif last_file.endswith(".pptx"):
            content = file_tools.read_pptx(last_file)
        else:
            content = file_tools.read_file(last_file)

        return summarize_text(content)

    except Exception as e:
        return f"Error summarizing file: {str(e)}"