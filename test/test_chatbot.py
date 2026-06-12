import os
import pytest
from dotenv import load_dotenv
from ai_chat_demo.chatbot import ChatBot

load_dotenv()


class TestChatBot:
    @pytest.fixture
    def bot(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        if not api_key:
            pytest.skip("未设置 ANTHROPIC_API_KEY")
        return ChatBot(api_key, base_url)

    def test_returns_string(self, bot):
        result = bot.chat("说 Hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_math(self, bot):
        assert "2" in bot.chat("1+1=?")