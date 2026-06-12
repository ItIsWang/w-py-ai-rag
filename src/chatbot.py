import os
from anthropic import Anthropic


class ChatBot:
    def __init__(self, api_key: str, base_url: str):
        self.client = Anthropic(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = "glm-5.1"

    def chat(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # 遍历所有内容块，只取 TextBlock 的文本
        for block in response.content:
            if block.type == "text":
                return block.text
        # 如果没有文本块，返回空字符串
        return ""
