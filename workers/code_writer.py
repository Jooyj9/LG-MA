"""CodeWriter Agent —— 根据需求编写代码并写入文件。"""

from langchain.agents import create_agent
from llm import llm
from tools import write_file, read_file


def create_code_writer() -> create_agent:
    """创建 CodeWriter Agent。

    职责单一：根据任务写代码、保存到文件。
    不负责审查、不负责测试。
    """
    return create_agent(
        model=llm,
        tools=[write_file, read_file],
        name="code_writer",
        system_prompt=(
            "你是一位资深Python开发者。"
            "根据任务需求，编写清晰、有文档、可直接运行的代码，"
            "并使用 write_file 保存到文件。"
            "写完代码后，在脑中验证逻辑正确性。"
            "最终输出完整的代码内容。"
            "只负责写代码，不要审查或测试。"
        ),
    )
