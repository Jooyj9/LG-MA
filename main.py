"""入口 —— v0.1: Supervisor + CodeWriter 最小闭环。

架构（从下至上）：
    tools/        → 基础工具（文件读写）
    state.py      → 共享 State 定义
    llm.py        → LLM 配置
    workers/      → 各 Worker Agent
    supervisor.py → 任务调度
    main.py       → 入口（你现在在这里）
"""
from supervisor import create_app


def main():
    app = create_app()

    task = input("Task: ").strip()
    if not task:
        task = "写一个判断字符串是否为回文的Python函数，包含测试用例。"

    print(f"\n{'='*60}")
    print(f"Task: {task}")
    print(f"{'='*60}\n")

    result = app.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"configurable": {"thread_id": "demo-1"}},
    )

    for msg in result["messages"]:
        role = getattr(msg, "name", None) or getattr(msg, "type", "?")
        content = getattr(msg, "content", str(msg))
        if content:
            print(f"\n── [{role}] ──")
            print(content[:800])


if __name__ == "__main__":
    main()
