# LLM-Powered File System Assistant

An LLM-powered assistant that manages resume files using tool/function calling.
Built with Python, OpenRouter (OpenAI-compatible API), and file parsing libraries
for PDF, TXT, and DOCX formats.

## Features

**Part A: Core File System Tools** (`fs_tools.py`)
- `read_file(filepath)` — Reads PDF, TXT, or DOCX files and extracts text content
- `list_files(directory, extension=None)` — Lists files in a directory, optionally filtered by extension
- `write_file(filepath, content)` — Writes content to a file, creating directories if needed
- `search_in_file(filepath, keyword)` — Case-insensitive keyword search with surrounding context

**Part B: LLM Integration** (`llm_file_assistant.py`)
- Connects the above tools to an LLM via OpenRouter's function-calling API
- Supports multi-step tool calling — the LLM can call multiple tools in sequence
  (e.g., list files, then search each one) before producing a final answer

## Setup

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Get an OpenRouter API key from [openrouter.ai/keys](https://openrouter.ai/keys)

3. Set your API key as an environment variable:
```bash
   export OPENROUTER_API_KEY="your-key-here"
```
   (In Google Colab, use Colab Secrets instead.)

## Usage

```python
from openai import OpenAI
from llm_file_assistant import run_assistant

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-key-here",
)

tools_schema = [...]  # see notebook for full tool schema definitions

answer = run_assistant("List all the files in the resumes folder", client, tools_schema)
print(answer)
```

## Example Queries

- "List all the files in the resumes folder"
- "Find resumes mentioning Python experience"
- "Read resume_john_doe.txt and create a summary file called summary_john_doe.txt in the output folder"

## Project Structure
.
├── fs_tools.py # Core file system tools
├── llm_file_assistant.py # LLM integration + tool-calling loop
├── requirements.txt # Python dependencies
├── resumes/ # Sample resume files (PDF, TXT, DOCX)
├── output/ # Generated output files (summaries, etc.)
└── README.md
## Known Limitations

- `search_in_file` performs simple case-insensitive keyword matching, not semantic
  understanding — e.g., it cannot distinguish "has Python experience" from
  "no Python experience." The LLM layer partially compensates for this by reasoning
  over the raw matches.
- The LLM's tool-calling behavior depends on the underlying model's reasoning quality;
  simpler/cheaper models may occasionally take shortcuts (e.g., assuming a file
  extension without checking).
