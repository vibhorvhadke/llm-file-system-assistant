# Cell 4: Write fs_tools.py — the core file system tools module.
# This file defines 4 functions the LLM will later call:
#   - read_file       : extract text from a PDF/TXT/DOCX file
#   - list_files      : list files in a directory, optionally filtered by extension
#   - write_file      : write text content to a file (creates folders if needed)
#   - search_in_file   : case-insensitive keyword search with surrounding context

import os
from pypdf import PdfReader
from docx import Document


def read_file(filepath: str) -> dict:
    """
    Read a resume file (PDF, TXT, or DOCX) and extract its text content.
    Returns a structured dict with content and metadata.
    """
    if not os.path.exists(filepath):
        return {"success": False, "error": f"File not found: {filepath}"}

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif ext == ".pdf":
            reader = PdfReader(filepath)
            content = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif ext == ".docx":
            doc = Document(filepath)
            content = "\n".join(para.text for para in doc.paragraphs)

        else:
            return {"success": False, "error": f"Unsupported file type: {ext}"}

        return {
            "success": True,
            "filepath": filepath,
            "extension": ext,
            "content": content,
            "length": len(content)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def list_files(directory: str, extension: str = None) -> list:
    """
    List files in a directory, optionally filtered by extension.
    Returns a list of dicts with file metadata.
    """
    if not os.path.isdir(directory):
        return [{"success": False, "error": f"Directory not found: {directory}"}]

    files_info = []
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)

        if not os.path.isfile(full_path):
            continue

        if extension and not name.lower().endswith(extension.lower()):
            continue

        stat = os.stat(full_path)
        files_info.append({
            "name": name,
            "size_bytes": stat.st_size,
            "modified": stat.st_mtime
        })

    return files_info


def write_file(filepath: str, content: str) -> dict:
    """
    Write content to a file. Creates parent directories if they don't exist.
    Returns a dict with success/failure status.
    """
    try:
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "filepath": filepath,
            "bytes_written": len(content.encode("utf-8"))
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def search_in_file(filepath: str, keyword: str, context_chars: int = 40) -> dict:
    """
    Search for a keyword inside a file's content (case-insensitive).
    Returns matches with surrounding context text.
    """
    file_result = read_file(filepath)

    if not file_result.get("success"):
        return file_result  # propagate the error (file not found, unsupported type, etc.)

    content = file_result["content"]
    lower_content = content.lower()
    lower_keyword = keyword.lower()

    matches = []
    start = 0
    while True:
        idx = lower_content.find(lower_keyword, start)
        if idx == -1:
            break

        context_start = max(0, idx - context_chars)
        context_end = min(len(content), idx + len(keyword) + context_chars)
        snippet = content[context_start:context_end].replace("\n", " ")

        matches.append({
            "position": idx,
            "context": snippet
        })
        start = idx + len(keyword)

    return {
        "success": True,
        "filepath": filepath,
        "keyword": keyword,
        "match_count": len(matches),
        "matches": matches
    }
