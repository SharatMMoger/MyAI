"""
Natural-language command task: turns free phrasing ("25 ka square root nikalo")
into one of MyAI's commands, runs it, and otherwise falls back to plain LLM chat.
Register it right before llm_fallback.
"""
import re
import dispatcher
from llm_tool import ask_llm, chat_llm

KNOWN_COMMANDS = ("sqrt ", "power ", "factorial ", "gcd ", "lcm ",
                  "readpdf ", "summarize it", "progress")

HINTS = re.compile(r"\d|\.pdf|\.txt|\.docx|summar|progress", re.IGNORECASE)

PROMPT = """Convert the user's request into ONE command for a small assistant, or answer NONE.
Commands:
sqrt <number>
power <base> <exponent>
factorial <number>
gcd <a> <b>
lcm <a> <b>
readpdf <filename>
summarize it
progress
The request may be in English, Hindi or Hinglish. If it clearly matches a command, output only that command. Otherwise output only NONE.
Request: {q}"""


def can_handle(question):
    return True


def _rewrite(question):
    reply = ask_llm(PROMPT.format(q=question), system_prompt="You output a single command or NONE, nothing else.")
    lines = reply.strip().splitlines()
    if not lines:
        return None
    command = lines[0].strip().lower()
    return command if command.startswith(KNOWN_COMMANDS) else None


def run(question, context):
    if not context.get("nl_rewritten") and HINTS.search(question):
        command = _rewrite(question)
        if command:
            result = dispatcher.dispatch(command, {"nl_rewritten": True})
            if result:
                return result
    return chat_llm(question)