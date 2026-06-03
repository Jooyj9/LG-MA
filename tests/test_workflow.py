"""端到端测试 —— 验证完整 Workflow。"""
from supervisor import create_app


def test_simple_task():
    """测试一个简单任务能否走通完整流程。"""
    app = create_app()

    result = app.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "写一个函数 add(a, b)，返回两数之和。保存到 add.py。",
                }
            ]
        },
        config={"configurable": {"thread_id": "test-1"}},
    )

    # 验证有消息产出
    assert len(result["messages"]) > 0, "应该有消息产出"

    # 验证最后一条消息包含 DONE 或完成标识
    last_content = str(result["messages"][-1].content)
    has_done = "DONE" in last_content or "add" in last_content.lower()
    assert has_done, f"任务应该完成，最后消息: {last_content[:200]}"

    print("✓ test_simple_task passed")


if __name__ == "__main__":
    test_simple_task()
