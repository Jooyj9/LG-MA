"""LLM 配置 —— 全局单例，所有模块共用。"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MOONSHOT_MODEL", "kimi-k2.6"),
    base_url=os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1"),
    api_key=os.getenv("MOONSHOT_API_KEY"),
    temperature=0.6,  # Kimi K2.6: 0.6 with thinking disabled
    extra_body={"thinking": {"type": "disabled"}},
)
