"""v0.1: Supervisor + CodeWriter —— 最小可行版本

使用 Kimi K2.6 (OpenAI-compatible) 作为 LLM backend。
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool

load_dotenv()

# ============================================================
# LLM: Kimi K2.6 (OpenAI-compatible)
# ============================================================
llm = ChatOpenAI(
    model=os.getenv("MOONSHOT_MODEL", "kimi-k2.6"),
    base_url=os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1"),
    api_key=os.getenv("MOONSHOT_API_KEY"),
    temperature=0.6,  # Kimi K2.6: 0.6 with thinking disabled, 1.0 with thinking enabled
    extra_body={"thinking": {"type": "disabled"}},  # disable thinking to avoid reasoning_content issues
)


# ============================================================
# Tools
# ============================================================
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


# ============================================================
# Worker Agent: CodeWriter
# ============================================================
code_writer = create_agent(
    model=llm,
    tools=[write_file, read_file],
    name="code_writer",
    system_prompt=(
        "You are a senior Python developer. "
        "Given a task, write clean, well-documented, working code "
        "and save it to a file using write_file. "
        "Test the code mentally before finalizing. "
        "When done, output the final code."
    ),
)


# ============================================================
# Supervisor
# ============================================================
supervisor = create_supervisor(
    agents=[code_writer],
    model=llm,
    prompt=(
        "You are a team supervisor managing a Python developer. "
        "Assign coding tasks to code_writer. "
        "When code is ready and saved to file, respond with:\n"
        "'DONE: <brief summary of what was built>'."
    ),
)


# ============================================================
# Compile & Run
# ============================================================
def main():
    app = supervisor.compile(checkpointer=InMemorySaver())

    task = input("Task: ").strip()
    if not task:
        task = "Write a Python function that checks if a string is a palindrome. Include test cases."

    print(f"\n{'='*60}")
    print(f"Task: {task}")
    print(f"{'='*60}\n")

    result = app.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"configurable": {"thread_id": "demo-1"}},
    )

    # Print conversation
    for msg in result["messages"]:
        role = getattr(msg, "name", None) or getattr(msg, "type", "?")
        content = getattr(msg, "content", str(msg))
        if content:
            print(f"\n── [{role}] ──")
            print(content[:800])


if __name__ == "__main__":
    main()
