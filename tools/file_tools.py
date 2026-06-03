"""文件读写工具 —— 最基础的工具层，不依赖任何业务模块。"""
import os
from langchain_core.tools import tool


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file. Creates parent directories if needed.

    Args:
        path: File path (relative or absolute).
        content: The text content to write.
    """
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"[OK] Wrote {len(content)} bytes to {path}"


@tool
def read_file(path: str) -> str:
    """Read content of a file.

    Args:
        path: File path to read.
    """
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[ERROR] File not found: {path}"
