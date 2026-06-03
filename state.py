"""共享 State 定义 —— 所有模块的通信协议。

Worker 之间不直接对话，全部通过这个 State 交换信息。
"""
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class TeamState(TypedDict):
    """多 Agent 团队的共享状态。

    每个 Node 读取需要的字段，返回需要更新的字段。
    Supervisor 通过 next_worker 控制调度。
    """

    messages: Annotated[List[BaseMessage], add_messages]
    """对话历史，add_messages 自动追加而非覆盖"""

    task: str
    """当前任务描述"""

    code: str
    """CodeWriter 生成的代码"""

    review_feedback: str
    """CodeReviewer 的审查意见"""

    test_results: str
    """Tester 的测试结果"""

    next_worker: str
    """Supervisor 的调度决策"""

    iteration_count: int
    """迭代计数器，防止死循环"""
