"""Supervisor —— 任务调度中枢。

负责：
1. 接收用户需求
2. 决定下一个干活的 Worker
3. 检查是否完成

Supervisor 只管路由，不管 Worker 内部细节。
"""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph_supervisor import create_supervisor
from llm import llm
from workers import create_code_writer, create_code_reviewer, create_tester


_agents = [
    create_code_writer(),
    create_code_reviewer(),
    create_tester(),
]

_supervisor = create_supervisor(
    agents=_agents,
    model=llm,
    prompt=(
        "你是一个软件开发团队的 Supervisor。"
        "你的团队有三个成员：\n"
        "- code_writer: 写代码\n"
        "- code_reviewer: 审查代码\n"
        "- tester: 测试代码\n\n"
        "工作流程：\n"
        "1. 先将任务分配给 code_writer 编写代码\n"
        "2. 代码写完后，交给 code_reviewer 审查\n"
        "3. 如果审查有问题，交回 code_writer 修改\n"
        "4. 审查通过后，交给 tester 测试\n"
        "5. 测试不通过，交回 code_writer 修改\n"
        "6. 全部通过后，回复 'DONE: <摘要>'\n\n"
        "按这个流程逐步推进，不要跳步。"
    ),
)


def create_app():
    """编译并返回可运行的 Supervisor 图。

    Returns:
        编译后的 LangGraph app，可直接 invoke/stream。
    """
    return _supervisor.compile(checkpointer=InMemorySaver())
