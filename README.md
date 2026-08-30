# MyAI — General-Purpose AI Assistant

A general-purpose AI assistant built in Python, combining rule-based tools with LLM intelligence (via Groq API). Built for the Razorpay AI Buildathon (Open Track).

## Features

- **LLM-Powered Conversations** — General questions answered intelligently using Groq's LLaMA-based models
- **Document Reading** — Reads PDF, TXT, DOCX, XLSX, and PPTX files
- **Document Summarization** — Summarizes any opened document using LLM
- **Document Q&A** — Ask specific questions about an opened document, get accurate answers grounded in its content
- **Calculator** — Handles arithmetic, trigonometry, statistics, probability, complex numbers, vectors, matrices, and calculus (via SymPy)
- **Memory** — Remembers facts across the conversation (e.g., "remember my name is X")
- **Context Awareness** — Tracks last opened file, last answer, and conversation history

## Tech Stack

- **Language:** Python
- **LLM:** Groq API (openai/gpt-oss-120b model)
- **Libraries:** `groq`, `python-dotenv`, `sympy`, and custom NLP/parsing modules

## Setup Instructions

1. Clone the repository: