"""
File reading task — handles readpdf, read, readdocx, readexcel, readppt commands.
Also updates context (last_file) so other tasks (summarize, ask) can use it.
"""
import file_tools
import context_state


def can_handle(question):
    q = question.lower().strip()
    prefixes = ["readpdf ", "read ", "readdocx ", "readexcel ", "readppt "]
    return any(q.startswith(p) for p in prefixes)


def run(question, context):
    q = question.strip()
    q_lower = q.lower()

    try:
        if q_lower.startswith("readpdf "):
            filename = q[8:].strip()
            context_state.set_value("last_file", filename)
            return file_tools.read_pdf(filename)

        if q_lower.startswith("readdocx "):
            filename = q[9:].strip()
            context_state.set_value("last_file", filename)
            return file_tools.read_docx(filename)

        if q_lower.startswith("readexcel "):
            filename = q[10:].strip()
            context_state.set_value("last_file", filename)
            return file_tools.read_excel(filename)

        if q_lower.startswith("readppt "):
            filename = q[8:].strip()
            context_state.set_value("last_file", filename)
            return file_tools.read_pptx(filename)

        if q_lower.startswith("read "):
            filename = q[5:].strip()
            context_state.set_value("last_file", filename)
            return file_tools.read_file(filename)

    except Exception as e:
        return f"Error reading file: {str(e)}"

    return None