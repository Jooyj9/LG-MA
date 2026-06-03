"""Tester Agent —— 为代码生成并运行测试。"""

from langchain.agents import create_agent
from llm import llm
from tools import read_file, write_file


def create_tester() -> create_agent:
    """创建 Tester Agent。

    职责单一：读代码、写测试、运行并报告结果。
    """
    return create_agent(
        model=llm,
        tools=[read_file, write_file],
        name="tester",
        system_prompt=(
            "你是一位QA工程师。读取代码文件后：\n"
            "1. 为代码编写单元测试\n"
            "2. 将测试写入 test_<原文件名>.py\n"
            "3. 说明如何运行测试以及预期的结果\n"
            "只负责测试，不要修改业务代码。"
        ),
    )
