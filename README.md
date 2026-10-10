# MyAI: Modular AI Assistant with Task Tracking and Goal Execution

A modular AI assistant in Python that combines deterministic tools (calculator, file readers) with LLM intelligence (via the Groq API). Tasks run through a dispatcher, every task is tracked and verified, and complex requests can be broken into steps and executed automatically.

## Features

- **LLM-powered chat**: general questions answered through Groq (`openai/gpt-oss-120b`), including Hindi and Hinglish
- **Document reading**: PDF, TXT, DOCX, XLSX, PPTX
- **Summarization**: `summarize it` summarizes the last opened file
- **Document Q&A**: `ask <question>` answers strictly from the last opened document
- **Document comparison**: `compare a.pdf and b.pdf` highlights similarities and differences
- **Calculator**: arithmetic, trigonometry, statistics, probability, vectors, matrices and calculus (SymPy)
- **Persistent memory**: facts saved with `remember ... is ...` survive restarts (stored in `user_memory.json`)
- **Task tracking**: every task is logged as RUNNING, COMPLETED or FAILED, with a progress bar
- **Self-verification**: tasks can define a `verify` function, so a result only counts as success if it is genuinely valid
- **Retry**: a failed task is retried once automatically
- **Goal execution**: `goal: ...` breaks a request into steps with the LLM, runs each step, stops on the first failure, and reports progress

## Commands

| Command | What it does |
|---|---|
| `sqrt 25`, `power 2 10`, `factorial 5`, `gcd 12 18` | Calculator |
| `readpdf file.pdf`, `read file.txt`, `readdocx`, `readexcel`, `readppt` | Open a file |
| `summarize it` | Summarize the last opened file |
| `ask what is the course name?` | Question about the last opened file |
| `compare a.txt and b.txt` | Compare two documents |
| `remember my name is Sharat` / `what is my name` | Save and recall a fact |
| `goal: read file.pdf and then summarize it` | Multi-step goal with a report |
| `progress` | Completed / failed counts and progress bar |
| `task history` | Last 10 task events |
| `reset progress` | Clear task history |
| anything else | Answered by the LLM |

## Example: goal execution

```
Ask me something: goal: read cn front page (1).pdf and then summarize it

Goal: read cn front page (1).pdf and then summarize it

Step 1: readpdf cn front page (1).pdf → COMPLETED
Step 2: summarize it → COMPLETED

Goal Status: 2/2 steps completed (100.0%)
```

If a step fails (for example the file does not exist), the remaining steps are skipped and the report shows the failure instead of claiming success.

## Architecture

```
main.py
  └── dispatcher.py        register(name, can_handle, run, verify=None) / dispatch(question)
        ├── task_tracker.py     logs status to task_history.json, computes progress
        └── tasks/
              ├── goal_task.py            goal → LLM planner → steps → verify → report
              ├── calculator_task_v2.py   uses math_tools.py (has its own verify function)
              ├── file_reading_task.py    uses file_tools.py, sets last opened file
              ├── summarize_task_v2.py    LLM summary of last file
              ├── ask_task_v2.py          LLM Q&A grounded in last file
              ├── memory_task_v2.py       uses memory.py (JSON storage)
              ├── compare_task.py         LLM document comparison
              ├── progress_task.py        progress, task history, reset
              └── llm_fallback_task.py    catch-all, always registered last
llm_tool.py                Groq client: ask_llm, summarize_text, answer_question, break_into_steps
```

How a request flows: `main.py` sends the question to the dispatcher, which runs the first registered task whose `can_handle` matches. The result is checked by the task's `verify` function (or a generic failure heuristic), logged by the tracker, and returned.

Registration order matters: `goal` is registered first, and `llm_fallback` last.

`brain.py` and its helper modules are the earlier rule-based version of the assistant, kept for reference. `main.py` no longer uses them.

## Setup

1. Clone the repository:
```
   git clone https://github.com/SharatMMoger/MyAI.git
   cd MyAI
```
2. Install dependencies:
```
    pip install -r requirements.txt
```
3. Create a `.env` file in the same folder as `llm_tool.py`:
```
   GROQ_API_KEY=your_api_key_here
```
   Get a free key at [console.groq.com](https://console.groq.com). Never commit this file.
4. Run from the folder that contains the files you want to open:
```
   python main.py
```
   File commands look for files relative to the folder you run from.

## Roadmap

- LLM-based intent classification (natural phrasing like "25 ka square root nikalo")
- Verify functions for more tasks, and smarter recovery when a step fails
- OCR for scanned documents
- Advisory-only medical, financial and coding modules (information and guidance, never diagnosis or financial advice)