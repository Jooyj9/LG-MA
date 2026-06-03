"""CodeReviewer Agent —— 审查代码的 Bug、风格和边界情况。"""

from langchain.agents import create_agent
from llm import llm
from tools import read_file


def create_code_reviewer() -> create_agent:
    """创建 CodeReviewer Agent。

    职责单一：读代码、找问题、给具体反馈。
    不负责修改代码。
    """
    return create_agent(
        model=llm,
        tools=[read_file],
        name="code_reviewer",
        system_prompt=(
            "你是一位代码审查者。读取代码文件，检查以下方面：\n"
            "1. Bug 和逻辑错误\n"
            "2. 代码风格和可读性\n"
            "3. 边界情况和错误处理\n"
            "4. 性能问题\n\n"
            "给出具体的、可操作的反馈，指出文件名和行号。"
            "只审查，不要修改代码。"
        ),
    )
